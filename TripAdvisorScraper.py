from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import csv


with open('EmailListGAU.csv', 'w') as f:
    f.write("Name, Email, URL \n")


y = 30

def emailExtractor(urlString):
    getH=requests.get(urlString)
    h=getH.content
    soup=BeautifulSoup(h,'html.parser')
    try:
        name = soup.find(attrs={'data-test-target':'top-info-header'}).get_text()
    except:
        name = "NA"

    mailtos = soup.select('a[href^=mailto]')
    
    for i in mailtos:
        href=i['href']
        try:
            str1, str2 = href.split(':')
            str2 = str2.split('?')
        except ValueError:
            break
        with open('EmailListGAU.csv', 'a') as f:
            f.write(name + "," + str2[0] + "," + urlString + "\n")

links = []
CL = []


for i in range(1,159):
    print(i)
    x = str(y * i)
    URL = "https://www.tripadvisor.co.za/Restaurants-g312568-oa" + x + "-Gauteng.html#EATERY_LIST_CONTENTS"
    # Open FireFox
    driver = webdriver.Firefox()
    # Go to URL
    driver.get(URL)

    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        links.append(elem.get_attribute("href"))
    for link in links:
        if link.startswith('https://www.tripadvisor.co.za/Restaurant_Review') and link.endswith('.html'):
            CL.append(link)
    driver.close()

SCL = set(CL)

for q in SCL:
    with open('SCL.csv', 'a') as f:
        f.write(q + "\n")

print("Length of SCL")
print(len(SCL))
for val in SCL:
    emailExtractor(val)

print("Scraping Completed")