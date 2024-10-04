"""
This script looks for index.html files
In the top level index.html file with all the images  it loops through <div class = "post-feed-grid">
looking for poster, preview, download, and sticker image urls.
In the index.html files that are in the 'p' folder, it finds the p_class = transparent loaded or main_class = post-cell
and grabs the url.
These urls are passed to requests.get which returns the contents of the image file.
Otherwise the URL is chopped up to get filename
Then look for filename in ImageFiles folder to prevent duplicate downloads
If not in ImageFiles get contents
Get the alt-text post-cell Get creator info from -- ('span[data-v-bee853a2=""]').text
"""

from bs4 import BeautifulSoup
import re
import csv
import os

import requests
from urllib.parse import unquote
from pathlib import Path
from time import sleep

posterList = []

posterPattern = "(appspot.com/o/)(.*)(\\?alt)"

def pImages(sp):

    pImage = sp.find("img", class_="bg-transparent loaded")


    if pImage != None:
        overlayUrl = pImage["src"]

        if overlayUrl:
            #imageType = "Overlay"
            #posterInfo['OverlayFilename'] = getFiles(overlayUrl, imageType)
            getFiles(overlayUrl)
def mainImages(sp):
    postercount = 0
    imageDivs = sp.find_all("div", class_="post-cell")
    for image in imageDivs:
        posterInfo = {}
        previewUrl = image.find("img", class_="h-full w-full object-cover")["data-src"]
        if previewUrl:
            postercount += 1
            posterInfo['PreviewFilename'] = getFiles(previewUrl)
            print(previewUrl)
            print(postercount)

        posterUrl = image.find("a", class_="download button compact")["href"]
        #print(unquote(posterUrl))
        if posterUrl:
            posterInfo['PosterFilename'] = getFiles(posterUrl)
            posterInfo['creator'] = image.select_one('span[data-v-bee853a2=""]').text

        stickerDiv = image.find("div", class_="post-overlay sticker")
        if stickerDiv:
            stickerUrl = stickerDiv.find("img")["data-src"]
            posterInfo['StickerFilename'] = getFiles(stickerUrl)

        posterList.append(posterInfo)
    return
    #print(posterList)
def getFiles(url):

    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            files = requests.get(url, timeout=10, stream=True)
            break  # Exit loop if request is successful

        except requests.exceptions.ReadTimeout:
            print(f"Timeout occurred, retrying... ({retry_count + 1})")
            sleep(2)  # Wait for 2 seconds before retrying
            retry_count += 1

    if url.find('/'):
        shortReg = re.search(posterPattern, unquote(url)) #Replace %xx escapes with their single-character equivalent.
        fileLoc = shortReg.group(2)

        filepath = Path("../ImageFiles/" + fileLoc)
        #print(filepath)
        #checking for existance of the filepath before downloading
        if os.path.isfile(filepath):
            #print("File exists")
            return filepath
            pass
        else:
            #print("does not exist")
            output_file = Path("../ImageFiles/" + fileLoc)
            output_file.parent.mkdir(exist_ok=True, parents=True)
            output_file.open("wb").write(files.content)
            return output_file

for root, dirs, files in os.walk("../", topdown=False):
    for name in files:
        iPath = os.path.join(root, name)
        if iPath.endswith('index.html'):
            with open(iPath) as f:
                soup = BeautifulSoup(f, "html.parser")
                if "/p/" in root: # this can be removed
                    #print(iPath)
                    pImages(soup)

                else:
                    #print(iPath)
                    mainImages(soup)

with open('BelArts.csv', 'w') as artFile:
    artWrite = csv.DictWriter(artFile, fieldnames=['StickerFilename',"PreviewFilename", "PosterFilename", "creator"])
    artWrite.writeheader()
    artWrite.writerows(posterList)

print('done')





