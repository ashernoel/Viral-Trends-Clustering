
# skepitcal this data exists specificallt identify searches in your area

from googleTrendsUpgrade import *
import urllib
import re
from bs4 import BeautifulSoup
import operator
import requests
import time

import string

wordList = []
google_url = "https://trends.google.com/trends/explore?geo=US-NH-517&q=harvard%20University"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
source_code = requests.get(google_url, headers=headers).text
soup = BeautifulSoup(source_code, 'html.parser')
print(soup)
for each_text in soup.findAll('div', {'class': 'widget-template'}):
    content = each_text.text.lower()
    print(content)
    if ("charlotte" in content):
        print(google_url)
    time.sleep(.5)


#checked for 000-009 manually lolz

for x in range(100):
    cambridge = []
    google_url = "https://trends.google.com/trends/explore?geo=US-NH-0" + str(x) + "&q=harvard%20University"
    source_code = requests.get(google_url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    print(soup)
    for each_text in soup.findAll('div', {'class':'entry-content'}):
        content = each_text.text.lower()

        if("charlotte" in content):
            print(google_url)

for x in range(100, 1000):
    cambridge = []
    google_url = "https://trends.google.com/trends/explore?geo=US-NH-" + str(x) + "&q=harvard%20University"
    source_code = requests.get(google_url).text
    soup = BeautifulSoup(source_code, 'html.parser')
    print(soup)
    for each_text in soup.findAll('div', {'class':'entry-content'}):
        content = each_text.text.lower()

        if("charlotte" in content):
            print(google_url)

