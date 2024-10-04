from selenium import webdriver
import time

browser = webdriver.Chrome()

browser.get('https://cultprotest.me/')

time.sleep(20)
html2 = browser.execute_script("return document.documentElement.outerHTML;")
print(html2)