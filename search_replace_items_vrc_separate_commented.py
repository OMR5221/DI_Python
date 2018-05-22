import sys
from sets import Set # Set: only contains unique elements

#Take as input a list of files to run the search and replace over: output from shell script which finds all markers,
# diveplans, diveboks, etc...
if(len(sys.argv) < 2):
    print('Usage: search_replace_items_vrc_separate.py <file list>')
    sys.exit()

# Get the name of the file conatining .dvp, .mrk, .dpt files
fileListFileName = sys.argv[1]

# Firt portion of this filename containing a list of files
baseName = fileListFileName.split('.')[0]

#The names of the log files are based on the name of the input file
replacedFileName = baseName + '_replaced.txt'
errorFileName = baseName + '_errors.txt'

#Expects the VRC file to be in the same directory
# File containig columns with old and new vrc values
vrcFile = open("original_new_vrc.txt")

vrcHeaders = vrcFile.readline()

#Store the old/new VRC values in a dictionary
# We are creating a dictionary to map one old value to a single new value, otherwise write out as an inconsistency
searchReplaceVrcDict = {}

#This was used to check for values where the same old value mapped to more than one new value, which I called "inconsistent" 
#These values were send to Renee and she selected which ones to use
# Mapped to a set which can only contain unique elements so values only shown once
nonConsistentValues = Set()

#Read in the VRC file and store the old/new values in the dictionary, checking for inconsistencies 
#Also checked for values with " in the name -- included both the raw old/new values as well as \\\" replacing the "
for line in vrcFile:
    sLine = line.strip().split('\t') # Automatically splits into a list
    originalVrc = sLine[0]
    newVrc = sLine[1]
    if originalVrc in searchReplaceVrcDict: # Check if originalVrc already in dictionary
      # If originalVrc already in here and the newVrc does not match then inconsistency found
        if newVrc != searchReplaceVrcDict[originalVrc]:
            print('WARNING inconsistent VRC!')
            print(originalVrc + ' : ' + newVrc)
            print(originalVrc + ' : ' + searchReplaceVrcDict[originalVrc])
            nonConsistentValues.add(originalVrc) # Add inconsistent originalVrc to Set() 

   # For each element check if contains "
    if '"' in originalVrc or '"' in newVrc:
        searchReplaceVrcDict[originalVrc.replace('"', '\\\\\\\"')] = newVrc.replace('"', '\\\\\\\"')

   # Set the originalVrc as key to the newVrc value
    searchReplaceVrcDict[originalVrc] = newVrc

vrcFile.close()

#The old/new Item values are stored in a two level dictionary
#The first maps sizes -> dictionary containing old/new values
searchReplaceItemDict = {}

#Also assumes the file is in the same directory
itemFile = open("original_new_items.txt")

# ets first line of file as a string
itemHeaders = itemFile.readline()

#Read in the old/new Item values and store in the dictionary appropriately, also checking for inconsistencies
#Also including \\\" versions of values with " in them
for line in itemFile:
    sLine = line.strip().split('\t')
    originalItem = sLine[0]
    newItem = sLine[1]
    size = sLine[2]

   # not in: operator tied to dictionaries
    if size not in searchReplaceItemDict:
        searchReplaceItemDict[size] = {}

   # Dictionary within a dictionary: Dictionary with Size key maps to a dictionary with a key of originalItem with value newItem
    searchReplaceDict = searchReplaceItemDict[size]

    if originalItem in searchReplaceDict:
#        print('WARNING: originalItem: ' + originalItem + ' is already in searchReplaceDict')
        if newItem != searchReplaceDict[originalItem]:
            print('WARNING inconsistent Item!')
            print(originalItem + ' : ' + newItem)
            print(originalItem + ' : ' + searchReplaceDict[originalItem]) 
            nonConsistentValues.add(originalItem)

    if '"' in originalItem or '"' in newItem:
#        print(originalItem.replace('"', '\\\\\\\"') + ' : ' + newItem.replace('"', '\\\\\\\"'))
        searchReplaceDict[originalItem.replace('"', '\\\\\\\"')] = newItem.replace('"', '\\\\\\\"')


    searchReplaceDict[originalItem] = newItem

#print(searchReplaceItemDict)

itemFile.close()

#Commented out in the file version -- but here's where inconsistent values were found
#Remove any values where the original to new mapping is inconsistent
#for value in nonConsistentValues:
#    print(value)
#    print(searchReplaceDict[value])
#    del searchReplaceDict[value] 


#Now start reading in all of the files and search and replacing line by line
fileList = open(fileListFileName)
logFile = open(replacedFileName, 'w')
errLogFile = open(errorFileName, 'w')
numFiles = 1

for fileName in fileList:
    fileName = fileName.strip()
    matches = False
    try: # Try and open filename
        currFile = open(fileName)
        #store the new lines to be output if a match is found
        outFileLines = [] # Create a list of all lines to rewrite to output file
        
        print('File# ' + str(numFiles) + ' name: ' + fileName)
        numFiles = numFiles + 1 # Just keeps track of the number of files passed through
        
        #Go line by line doing the search/replace
        for line in currFile:
            #First check if '--' is in the line, if not continue to the next line
            if '--' not in line:
                outFileLines.append(line)
                continue
            
            #Go over all of the VRC values, there's a lot less of them so didn't do any additional checks
            # For each key value in dictionary, if in this line then replace originalVrc with newVrc 
            for origValue in searchReplaceVrcDict.keys():
                if origValue in line:
                    matches = True
                #                print('Matches: ' + origValue)
                    line = line.replace(origValue, searchReplaceVrcDict[origValue])

            #First check if the size value is in the line
            for size in searchReplaceItemDict.keys():
                #If the size value is in the line, then check any of the associated items are in the line
                if size in line:
                    for origItem in searchReplaceItemDict[size]:
                        if origItem in line:
                            matches = True
                            line = line.replace(origItem, searchReplaceItemDict[size][origItem])
                    
            outFileLines.append(line)

        currFile.close()

    #Catch any IO errors and write them out the log
    except IOError, err:
        errLogFile.write(str(err))

    if matches:
        logFile.write(fileName + '\n')
        outFile = open(fileName, 'w')
        outFile.write(''.join(outFileLines))
        outFile.close()

logFile.close()
fileList.close()
