#!/usr/bin/python

# os and os.path modules contain methods which interact with the system
import os
import re
from datetime import date, timedelta, datetime
from time import localtime

# Print both absolute and relative paths
def get_user_markers(dir):  
    
    # subprocess.call()

    # filenames = os.walk(dir) # list of files in the given dir
    
    fileNameList = []
	
    cutoff_date = datetime.now() - timedelta(days=16)
	
    cutoff_date = cutoff_date.timetuple()

    for root, subdirs, filenames in os.walk(dir):
        
        for file in filenames:
            
            if re.search(r'.*.(mrk|dbk|dvp)', file, re.IGNORECASE) != None:
		
		#filetime_secs = os.path.getmtime(root + '/' + file)
            
		#filedate = localtime(filetime_secs)
		
		#if filedate > cutoff_date:
		#	continue

		#else:
                file = file + '\n'
            
                filename = root + '/' + file
    
                fileNameList.append(filename)

            else:
                continue

        #for filename in filenames:

            #filename += filename + "\n"
            
            #fileNameList.append(filename)

      #print("Relative Path: " + os.path.join(dir, filename)) # Relative Path
      #print("Absolute Path: " + os.path.abspath(os.path.join(dir, filename))) # Absolute Path
    
    fileoutName = 'user_file_paths.txt'
    fileout = open(fileoutName, 'w')
    fileout.write(''.join(fileNameList))

def main():

    #printdir("/di/global/models/Users")
    get_user_markers("/di/global/models/Users")

if __name__=='__main__':
   main()
