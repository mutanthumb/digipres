# download image files linked from index.html in p folders
# if filename not in ImageFiles

from bs4 import BeautifulSoup
import re
import csv
import os

import glob

import requests
from urllib.parse import unquote
from pathlib import Path

posterList = []

posterPattern = "(appspot.com/o/)(.*)(\\?alt)"
overlayPattern = "(ImageFiles/)(.*)(\\?alt)"


# pImages function can be folded into the other function.
def pImages(sp):

    pImage = sp.find("img", class_="bg-transparent loaded")

    #print(pImage)

    if pImage != None:
        overlayUrl = pImage["src"]
        #print(unquote(overlayUrl))

        overlayFiles = requests.get(overlayUrl, stream=True)

        if overlayUrl.find('/'):
            shortReg = re.search(posterPattern, unquote(overlayUrl))
            OverlayFilename = shortReg.group(2)
            #print(OverlayFilename)
            nSplit = OverlayFilename.split("/", 1)

            pattern = nSplit[1]

            filepath = Path("../ImageFiles/" + OverlayFilename)
            print(filepath)
            if os.path.isfile(filepath):
                print("File exists")
                pass
            else:
                print("does not exist")
                output_file = Path("../ImageFiles/" + OverlayFilename)
                output_file.parent.mkdir(exist_ok=True, parents=True)
                output_file.open("wb").write(overlayFiles.content)


# Can this repetition be eliminated?
# make div types variables and pass those to functions
def mainImages(sp):
    imageDivs = sp.find_all("div", class_="post-cell")

    for image in imageDivs:
        posterInfo = {}

        previewUrl = image.find("img")["data-src"]
        print(unquote(previewUrl))
        posterUrl = image.find("a", class_="download button compact")["href"]
        print(unquote(posterUrl))


        stickerDiv = image.find("div", class_="post-overlay sticker")

        if stickerDiv:
            print("found a sticker!")
            stickerUrl = stickerDiv.find("img")["data-src"]
            print(stickerUrl)
            stickerFiles = requests.get(stickerUrl, stream=True)

            if stickerUrl.find('/'):
                shortReg = re.search(posterPattern, unquote(stickerUrl))
                posterInfo['StickerFilename'] = shortReg.group(2)

                filepath = Path("../ImageFiles/" + posterInfo['StickerFilename'])
                print(filepath)
                if os.path.isfile(filepath):
                    print("File exists")
                    pass
                else:
                    print("does not exist")
                output_file = Path("../ImageFiles/" + posterInfo['StickerFilename'])
                output_file.parent.mkdir(exist_ok=True, parents=True)
                output_file.open("wb").write(stickerFiles.content)



        previewFiles = requests.get(previewUrl, stream=True)

        posterFiles = requests.get(posterUrl, stream=True)

        if previewUrl.find('/'):

            shortReg = re.search(posterPattern, unquote(previewUrl))


            posterInfo['PreviewFilename'] = shortReg.group(2)
            filepath = Path("../ImageFiles/" + posterInfo['PreviewFilename'])
            print(filepath)
            if os.path.isfile(filepath):
                print("File exists")
                pass
            else:
                print("does not exist")
                output_file = Path("../ImageFiles/" + posterInfo['PreviewFilename'])
                output_file.parent.mkdir(exist_ok=True, parents=True)
                output_file.open("wb").write(previewFiles.content)

        if posterUrl.find('/'):
            #posterName = posterUrl.rsplit('/', 1)[1]
            #print(posterUrl)

            #longName = posterName + ".jpg" # try removing the .jpg
            shortReg = re.search(posterPattern, unquote(posterUrl))
            posterInfo['Filename'] = shortReg.group(2)

            filepath = Path("../ImageFiles/" + posterInfo['Filename'])
            print(filepath)
            if os.path.isfile(filepath):
                print("File exists")
                pass
            else:
                print("does not exist")
                output_file = Path("../ImageFiles/" + posterInfo['Filename'])
                output_file.parent.mkdir(exist_ok=True, parents=True)
                output_file.open("wb").write(posterFiles.content)
                posterInfo['creator'] = image.select_one('span[data-v-bee853a2=""]').text

        posterList.append(posterInfo)
    #print(posterList)

for root, dirs, files in os.walk("../", topdown=False):
    for name in files:
        iPath = os.path.join(root, name)
        if iPath.endswith('index.html'):
            with open(iPath) as f:
                soup = BeautifulSoup(f, "html.parser")
                if "/p/" in root: # this can be removed
                    print(iPath)
                    pImages(soup)

                else:
                    print(iPath)
                    mainImages(soup)

with open('BelArts.csv', 'w') as artFile:
    artWrite = csv.DictWriter(artFile, fieldnames=['StickerFilename',"PreviewFilename", "Filename", "creator"])
    artWrite.writeheader()
    artWrite.writerows(posterList)

print('done')





