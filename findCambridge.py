from googleTrendsUpgrade import *
import urllib
import re
from bs4 import BeautifulSoup
import operator
import requests

import string

wordList = []
google_url = "https://trends.google.com/trends/explore?geo=US-NH-517&q=harvard%20University"
source_code = requests.get(google_url).text
soup = BeautifulSoup(source_code, 'html.parser')
print(soup)
for each_text in soup.findAll('div', {'class':'entry-content'}):
    content = each_text.text.lower()
    print(content)
    if("Charlotte" in content):
        print(google_url)


"""
#checked for 000-009 manually lolz
for x in range(100):
    cambridge = []
    google_url = "https://trends.google.com/trends/explore?geo=US-NH-0" + str(x) + "&q=harvard%20University"
    openedPage = urllib.request.urlopen(google_url).read()
    instancesList = re.findall("Cambridge", openedPage)
    if len(instancesList) != 0:
        print(google_url)
"""