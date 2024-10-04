# https://stackoverflow.com/questions/31220131/find-and-replace-strings-in-html

from bs4 import BeautifulSoup
import re
import os


def indexWork(filepath):
    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f, "html.parser")
        hd = soup.head
        bd = soup.body
        #print(filepath)

        ogimage = hd.find("meta", property="og:image")
        ogimage["content"] = ogimage["content"].replace(
            "https://firebasestorage.googleapis.com/v0/b/cultprotest-me.appspot.com/o/",
            "http://localhost/cultprotest.me/ImageFiles/")

        blogChar = hd.find("script", charset="utf-8")
        # print(blogChar["src"])
        if blogChar != None:
            newLoc = "http://localhost/cultprotest.me" + blogChar["src"]
            blogChar["src"] = blogChar["src"].replace(blogChar["src"], newLoc)

        target = hd.find_all("link")
        for v in target:
            newURL = "http://localhost/cultprotest.me" + v["href"]
            # print(newURL)
            # print(type(v["href"]))
            v["href"] = v["href"].replace(v["href"], newURL)
            # print(v["href"])

        # <a class="" href="/p/
        pFolders = soup.findAll("a", class_="")
        for folder in pFolders:
            if folder.has_attr('href'):
                folder["href"] = folder["href"].replace("/p/", "http://localhost/cultprotest.me/p/")
        imageDivs = soup.findAll("img")
        for image in imageDivs:
            #print(image.text)
            if image.has_attr('data-src'):
                image["data-src"] = image["data-src"].replace(
                    "https://firebasestorage.googleapis.com/v0/b/cultprotest-me.appspot.com/o/",
                    "http://localhost/cultprotest.me/ImageFiles/")
            if image.has_attr('src'):
                print("found a src")
                image["src"] = image["src"].replace(
                    "https://firebasestorage.googleapis.com/v0/b/cultprotest-me.appspot.com/o/",
                    "http://localhost/cultprotest.me/ImageFiles/")

        # need to find downloads
        dImage = bd.find("a", class_="download button compact")
        #print(dImage)
        if dImage != None:
            dImage["href"] = dImage["href"].replace(
                "https://firebasestorage.googleapis.com/v0/b/cultprotest-me.appspot.com/o/",
                "http://localhost/cultprotest.me/ImageFiles/")

        # <script src="/js/chunk-vendors.3feb8360.js"></script>
        # <script src="/js/app.6ed2f8f9.js"></script>

        soup = str(soup).replace('<script src="/js/chunk-vendors.3feb8360.js"></script>',
                                 '<!--script src="/js/chunk-vendors.3feb8360.js"></script-->')
        soup = str(soup).replace('<script src="/js/app.6ed2f8f9.js"></script>',
                                 '<!--script src="/js/app.6ed2f8f9.js"></script-->')

        with open(filepath, 'w', encoding='utf-8') as updateFile:
            updateFile.write(str(soup))


for root, dirs, files in os.walk("../", topdown=False):
    for name in files:
        iPath = os.path.join(root, name)
        if iPath.endswith('index.html'):
            print(iPath)
            indexWork(iPath)

print('done')