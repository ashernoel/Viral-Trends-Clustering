import praw
from datetime3 import datetime
import nltk
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
import string

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import sent_tokenize
from nltk.corpus import brown


"""
Task List:
goal: make a line graph that takes a word and does sentimental analysis over time
- search for word in post and when posted
- apply sentimental analysis value to the word (nltk package) = y-axis
- figure out matlib and plot this thing (time = x-axis)
"""


def main(): #main is for testing, get rid of it for finished product
    feels2()

#buzzword is the word we're scraping for, depthOfSearch is how many found instances of buzzWord posts you want to return
#returns postname string
def scrapeReddit(buzzWord, depthOFfSearch):
    # Authemticating; reddit username & password (HGoogleAnalytics; HGoogleAnalytics123)
    reddit = praw.Reddit(client_id='TD0pUQKADQUD7g', client_secret='hR-rl_PCxFOVd4U5DSodu1yJN3M', user_agent='Reddit WebScrape')
    #justified pulling from hot posts ? (time & most upvoted)
    hot_posts = reddit.subreddit('all').search(buzzWord, limit=depthOFfSearch)
    for post in hot_posts:
        dateStr = str(get_date(post))
        return (post.title + ": " + dateStr)

#get post time & date
def get_date(submission):
	time = submission.created
	return datetime.fromtimestamp(time)

def feelings():
    nltk.download()
    n_instances = 100
    subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
    obj_docs = [(sent, 'obj') for sent in
    subjectivity.sents(categories='obj')[:n_instances]]
    len(subj_docs), len(obj_docs)

    train_subj_docs = subj_docs[:80]
    test_subj_docs = subj_docs[80:100]
    train_obj_docs = obj_docs[:80]
    test_obj_docs = obj_docs[80:100]
    training_docs = train_subj_docs + train_obj_docs
    testing_docs = test_subj_docs + test_obj_docs
    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
    len(unigram_feats)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)
    trainer = NaiveBayesClassifier.train
    classifier = sentim_analyzer.train(trainer, training_set)
    for key, value in sorted(sentim_analyzer.evaluate(test_set).items()):
        print('{0}: {1}'.format(key, value))

def feels2():
    #nltk.download()
    text = scrapeReddit("halloween",1)
    tokenizedPhrase = sent_tokenize(text) #split into arrays of phrases
    tokenizedWord = nltk.tokenize.word_tokenize(text) #split into array of  words


    print(tokenizedPhrase)
    print(tokenizedWord)



main()
