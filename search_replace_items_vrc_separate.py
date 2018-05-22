import sys
from sets import Set

if(len(sys.argv) < 2):
    print('Usage: search_replace_items_vrc_separate.py <file list>')
    sys.exit()

fileListFileName = sys.argv[1]
baseName = fileListFileName.split('.')[0]
replacedFileName = baseName + '_replaced.txt'
errorFileName = baseName + '_errors.txt'

#print(replacedFileName)
#print(errorFileName)

vrcFile = open("original_new_vrc.txt")

vrcHeaders = vrcFile.readline()

searchReplaceVrcDict = {}

nonConsistentValues = Set()


for line in vrcFile:
    sLine = line.strip().split('\t')
    originalVrc = sLine[0]
    newVrc = sLine[1]
    if originalVrc in searchReplaceVrcDict:
        if newVrc != searchReplaceVrcDict[originalVrc]:
            print('WARNING inconsistent VRC!')
            print(originalVrc + ' : ' + newVrc)
            print(originalVrc + ' : ' + searchReplaceVrcDict[originalVrc])
            nonConsistentValues.add(originalVrc)

    if '"' in originalVrc or '"' in newVrc:
        searchReplaceVrcDict[originalVrc.replace('"', '\\\\\\\"')] = newVrc.replace('"', '\\\\\\\"')

    searchReplaceVrcDict[originalVrc] = newVrc

vrcFile.close()

searchReplaceItemDict = {}

itemFile = open("original_new_items.txt")

itemHeaders = itemFile.readline()


for line in itemFile:
    sLine = line.strip().split('\t')
    originalItem = sLine[0]
    newItem = sLine[1]
    size = sLine[2]

    if size not in searchReplaceItemDict:
        searchReplaceItemDict[size] = {}

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
    try:
        currFile = open(fileName)
        outFileLines = []
        
        print('File# ' + str(numFiles) + ' name: ' + fileName)
        numFiles = numFiles + 1
        
        for line in currFile:
            #        print('line: ' + line)
            if '--' not in line:
                outFileLines.append(line)
                continue
            
            for origValue in searchReplaceVrcDict.keys():
                if origValue in line:
                    matches = True
                #                print('Matches: ' + origValue)
                    line = line.replace(origValue, searchReplaceVrcDict[origValue])

            for size in searchReplaceItemDict.keys():
                if size in line:
                    for origItem in searchReplaceItemDict[size]:
                        if origItem in line:
                            matches = True
                            line = line.replace(origItem, searchReplaceItemDict[size][origItem])
                    
            outFileLines.append(line)

        currFile.close()

    except IOError, err:
        errLogFile.write(str(err))

    if matches:
        logFile.write(fileName + '\n')
        outFile = open(fileName, 'w')
        outFile.write(''.join(outFileLines))
        outFile.close()

logFile.close()
fileList.close()
