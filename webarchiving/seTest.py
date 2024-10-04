from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pathlib import Path

url = 'https://cultprotest.me/'

driver = webdriver.Firefox()
overLayDriver = webdriver.Firefox()
driver.get(url)

# This gets the total height of the page by scrolling directly to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(10)
totalHeight = driver.execute_script("return document.body.scrollHeight")
print(totalHeight)

new_height = 0

# This section scrolls down the page at the rate of 900 pixels at a time to allow the images to load
while new_height < totalHeight:
   driver.execute_script("window.scrollBy(0, 900)") # note this is scrollBy NOT scrollTo
   new_height = driver.execute_script("return window.scrollY")
   print(new_height)
   if totalHeight - new_height < 900:
       driver.execute_script("window.scrollBy(0, 10)")
       new_height = driver.execute_script("return window.scrollY")
       print(new_height)
       if totalHeight - new_height < 10:
           break
   time.sleep(10)

html2 = driver.execute_script("return document.documentElement.outerHTML;")

with open('../index.html', 'w') as file:
    file.write(html2)

# This section captures the other index.html files that are referenced in the main index file.

elems = driver.find_elements(by=By.XPATH, value="//a[@href]")
for elem in elems:
    print(elem.get_attribute("href"))
    olUrl = elem.get_attribute("href")
    if olUrl.startswith('https://cultprotest.me/p/'):
        foldName = olUrl.split('p/', 2)
        overLayDriver.get(olUrl)
        time.sleep(5)
        olHtml = overLayDriver.execute_script("return document.documentElement.outerHTML;")
        output_file = Path("../p/" + foldName[1] + '/index.html')
        output_file.parent.mkdir(exist_ok=True, parents=True) # makes the directories if they don't exist
        output_file.open("w").write(olHtml)



print('done')