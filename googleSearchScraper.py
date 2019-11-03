import urllib
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


#INPUT: List of keyterms "inputList" and number of items to return for each keyword "dictionaryDepth"
#OUTPUT: a dictionary of dataframes with a key of the keyword and a value of a dataframe with "Title" and "Description"


def get_google_definitions(input_list, dictionary_depth):

    total_results = pd.DataFrame(columns=["Keywords", "Descriptions"])

    ua = UserAgent()

    for keyword in input_list:

        print(keyword)
        # Notice the " and ' around trade war! This ensures phrase matching.
        query = urllib.parse.quote_plus(f"{keyword}") # Format into URL encoding
        google_url = "https://www.google.com/search?q=" + query + "&num=" + str(dictionary_depth)
        response = requests.get(google_url, {"User-Agent": ua.random})
        soup = BeautifulSoup(response.text, 'html.parser')
        result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

        word_results = pd.DataFrame(columns=["Links", "Titles", "Descriptions"])

        for r in result_div:
            try:
                link = r.find('a', href=True)
                title = r.find('div', attrs={'class': 'vvjwJb'}).get_text()
                description =r.find('div', attrs={'class': 's3v9rd'}).get_text()[:150]
                if description != '' and title != '' and link != '':
                    word_results = word_results.append({"Links": link, "Titles": title, "Descriptions": description}, ignore_index=True)

            except:
                continue

        all_descriptions = word_results['Titles'].tolist()
        descriptions = ' '.join(all_descriptions)

        # Remove punctuation, lowercase, and tokenize
        tokens = word_tokenize(descriptions.translate(str.maketrans('', '', string.punctuation)).lower())
        ps = PorterStemmer()

        # Remove stop words and stem the sentence
        filtered_sentence = [ps.stem(w) for w in tokens if w not in {"wikipedia", "merriamwebst", 'britannicacom', 'dictionarycom'}.union(set(stopwords.words('english')))]

        print(filtered_sentence)

        # return a dataframe with the word as one column and a column with the descriptions as the second.
        total_results = total_results.append({"Keywords": keyword, "Descriptions": ' '.join(filtered_sentence)}, ignore_index=True)

    return total_results
