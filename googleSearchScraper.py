import urllib
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
import string

#INPUT: List of keyterms "inputList" and number of items to return for each keyword "dictionaryDepth"
#OUTPUT: a dictionary of dataframes with a key of the keyword and a value of a dataframe with "Title" and "Description"


def get_google_definitions(input_list, dictionary_depth):

    definitions = {}
    ua = UserAgent()

    for keyword in input_list:

        # Notice the " and ' around trade war! This ensures phrase matching.
        query = urllib.parse.quote_plus(f"{keyword}") # Format into URL encoding
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(dictionary_depth)
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, 'html.parser')
        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

        search_results = pd.DataFrame(columns=["Links", "Titles", "Descriptions"])

        for r in result_div:
            try:
                link = r.find('a', href=True)
                title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
                description =r.find('div', attrs={'class': 's3v9rd'}).get_text()[:150]
                if description != '' and title != '' and link != '':
                    search_results = search_results.append({"Links": link, "Titles": title, "Descriptions": description}, ignore_index=True)

            except:
                continue

        # Find the description that is most like a sentence, and choose that one for the classifier.
        best_index = 0
        old_punc = 150
        count = lambda l1, l2: sum([1 for x in l1 if x in l2])

        for index, row in search_results.iterrows():
            num_punc = count(row['Descriptions'], set(string.punctuation))
            if num_punc < old_punc:
                best_index = index
                old_punc = num_punc

        definitions[keyword] = search_results.loc[[best_index]]

        print(search_results.loc[best_index])

    return definitions
