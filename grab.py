#File Grabber by Anthony Pollard
#2022, No Copyright, Free for use

import csv
import shutil
import os
import logging

logging.basicConfig(filename='grab.log', level=logging.DEBUG)

print("Enter the name of the CSV file")
filename = input()
dest = 'C:\\Extract\\'
counter = 0
counterTotal = 0

isExist = os.path.exists(dest)
#Check if destination directory exists

if not isExist:
    os.makedirs(dest)
    logging.info('Destination Does Not Exist, Creating Directory at ', dest)

#Open csv file from input
with open(filename, 'r') as csvfile:
  datareader = csv.reader(csvfile)

  #loop through csv and pick out file locations
  for row in datareader:

      #check if file exists first and skip if it does
      rowName = (row[0].split("\\")[-1])
      localExist = os.path.exists(dest+rowName)
      if not localExist:
          print("Copying ... ", row[0])

          #try to copy it, throw error+log if issue with included failed row
          try:
              shutil.copy(row[0], dest)
              counter +=1

          except shutil.SameFileError:
              logging.warning('{a} already exists. Not copied.'.format(a=row[0]))
              print("File already exists.")
              counterTotal +=1
              pass

          except PermissionError:
              logging.warning('{a} has a permission issue. Not copied.'.format(a=row[0]))
              print("Permission denied.")
              counterTotal +=1
              pass

          except:
              logging.warning('{a} had an unknown error. Not copied.'.format(a=row[0]))
              print("Unspecified Error.")
              counterTotal +=1
              pass

      continue

missingFiles = counterTotal-counter

#list out summary and include in logfile
print("Loop Completed, a total of ", counter, "new rows were saved to: ",dest)
print(missingFiles, "are missing. Check grab.log")
logging.info('Loop Completed, a total of {a} rows were saved to: {b}'.format(a=counter, b=dest))
logging.info('{a} files are missing.'.format(a=missingFiles))
