"""
Python script to create metadata.csv for Arrived Digital:
Get name of Collection (source Rob or DLXS?)
Structure  = Folder of  data folders
Get name of folder = Filename : objects/Band-1
Open folder
Open *.csv file
Get Kaltura Entry ID
Get Program Title
Make dict with Filename, Collection, Program Title, Kaltura ID
Create metadata folder
Create metadata.csv with contents of dict
Save metadata.csv
"""

import csv
import os
from pathlib import Path

entries = Path('./hazen_preservation/')
for entry in entries.iterdir():
    #print(entry.name)
    if entry.is_dir():
        arrDigDict = {}
        arrDigDict['filename'] = 'objects/' + entry.name
        arrDigDict['Collection'] = "Hazen Schumacher's Jazz Revisited Radio Show"

        print(entry.name)
        mdPath = os.path.join(entry, 'metadata/')
        os.mkdir(mdPath)
        csvFile = mdPath + 'metadata.csv'
        for dirpath, dirnames, files in os.walk(entry):
            for file_name in files:
                if file_name.endswith('.csv'):
                    print(file_name)
                    with open(os.path.join(dirpath, file_name), "r") as adf:
                        reader = csv.DictReader(adf)
                        for row in reader:
                            if row['Kaltura Entry ID'] != '':
                                # print(row)
                                arrDigDict['Kaltura Entry ID'] = row['Kaltura Entry ID']

                            if row['Program Title'] != '':
                                arrDigDict['Program Title'] = row['Program Title']
                        print(arrDigDict)
                        with open(csvFile, 'w') as csvf:
                            w = csv.writer(csvf)
                            w.writerow(arrDigDict.keys())
                            w.writerow(arrDigDict.values())





