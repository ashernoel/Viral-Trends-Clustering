# Pytrends documentation: https://pypi.org/project/pytrends/
# Connect Pytrends API to google
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import string

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from wordfreq import zipf_frequency


# Remove the old hyper files from the last run time. Comment
# Connect with Google somehow
pytrends = TrendReq(hl='en-US', tz=360)

college_colors = {"Harvard University": "#A51C30",
                  "Stanford University": "#8C1515",
                  "Massachusetts Institute of Technology": "#8A8B8C",
                  "Princeton University": "#ff8f00",
                  "Yale University": "#0f4d92",
                  "Cornell University": "#D47500",
                  "Brown University": "#4E3629",
                  "Columbia University": "#B9D9EB",
                  "Dartmouth College": "#00693e",
                  "University of Pennsylvania": "tab:purple",

                  }


# Get the annual averages from the master data DataFrame
def getAnnualAverages(data, numYears, startingYear):
    frames = []
    for year in range(numYears):
        annualData = data.iloc[year*52:(year+1)*52]
        annualMean = annualData.mean().to_frame().T
        annualMean.index = annualMean.index + startingYear + year
        frames.append(annualMean)
    output = pd.concat(frames)

    # Normalize the annual averages so that they sum to 100
    output = output.div(output.sum(axis=1), axis=0)
    return output


def getTrendsData(keywords, region, timeframe, flagTopic):

    # FLAG: If FLAG = FALSE, keywords will be "Search Terms"
    #       If FLAG = TRUE, keywords will be the first "Topic" that comes up.
    # NOTE: keywords can NOT have duplicates!

    # Initialize flag and temporary list of quieries with the keyword that should be in all of them.
    old = 0
    tempList = [pytrends.suggestions(keywords[0])[0]['mid']] if flagTopic else [keywords[0]]

    # Initialize the datastructures
    trendData = pd.DataFrame()
    oldData = pd.DataFrame()

    for index in range(1, len(keywords)):

        # Add the next keyword in the list to the temporary list of queries
        keyword = keywords[index]

        # If the keyword does not have enough traffic, it will not be a topic; in these cases, add it as a search term.
        try:
            tempList.append(pytrends.suggestions(keyword)[0]['mid']) if flagTopic else tempList.append(keyword)
        except IndexError:
            tempList.append(keyword)

        # The maximum query request is five terms
        if index // 4 != old or (index == len(keywords) - 1):

            # Build the payload
            pytrends.build_payload(tempList, cat=0, timeframe=timeframe, geo=region, gprop='')

            newData = pytrends.interest_over_time()


            #Adjust the data so that the first column, the master column, has a maximum of 100
            maxMaster = newData[pytrends.suggestions(keywords[0])[0]['mid']].max() if flagTopic else newData[keywords[0]].max()

            newData.iloc[:, :-1] *= 100/(maxMaster)

            # Merge the old and new DataFrames
            if old == 0:
                oldData = newData.iloc[:, :-1]
                trendData = oldData
            else:
                try:
                    trendData = oldData.join(newData.iloc[:, 1:-1])
                except ValueError:
                    trendData = oldData.join(newData.iloc[:, 1:-1], lsuffix = '_left', rsuffix = '_right')
                oldData = trendData

            # Reset the temporary queries and increase the flag.
            tempList = [pytrends.suggestions(keywords[0])[0]['mid']] if flagTopic else [keywords[0]]
            old += 1


    # Update the columns of the trend data with the original names
    trendData.columns = keywords

    # Reorder the columns based off of their mean values.
    return trendData.reindex(trendData.mean().sort_values(ascending=False).index, axis=1)


def getRisingRelatedTopics(keyword, region, timeframe, cutoff):
    # Inputs:
        # keyword is a string format
        # region: "" for world, "US" for US
        # timeframe: YYYY-MM-DD YYYY-MM-DD format
        # cutoff: INT the % minimum % increase in searches over the period to be interesting (e.g., 100% = 100)

    pytrends.build_payload([pytrends.suggestions(keyword)[0]['mid']], cat=0, timeframe=timeframe, geo=region,
                           gprop='')
    topics = pytrends.related_topics()


    #Only return the topics above the cutoff
    return topics[pytrends.suggestions(keyword)[0]['mid']]['rising'].loc[topics[pytrends.suggestions(keyword)[0]['mid']]['rising']['value'] >= cutoff]

def getViralKeywords(keyword, region, timeframe, interval, cutoff):
    # INPUT: Timeframe in YYYY-MM-DD YYYY-MM-DD format

    keywords = [keyword]

    # Track the type of related topic
    keyword_types = []

    # Track the number of rising topics per time interval over time.
    virality = []



    # Add all of the related topics over that timeframe to the keywords list
    times = getTimeframes(timeframe[:10], timeframe[11:], interval)
    for time in times:
        topics = getRisingRelatedTopics(keyword, region, time, cutoff)
        keyword_types.extend(topics['topic_type'].tolist())
        keywords.extend(topics['topic_title'].tolist())

        virality.append(len(topics['topic_title'].tolist()))

    viralityPerQuarter = [0] * (len(virality)//6 + 1)
    for index, item in enumerate(virality):
        viralityPerQuarter[index // 6] += item
    print(viralityPerQuarter)
    print(virality)
    print(keyword_types)

    # Remove duplicates and punctuation from keywords:
    adjKeywords = []
    [adjKeywords.append(word.translate(str.maketrans('', '', string.punctuation))) for word in keywords if (word.translate(str.maketrans('', '', string.punctuation)) not in adjKeywords) and len(word) > 2]

    # Remove single words that are too common in english like Mother or July
    adj2Keywords = []
    [adj2Keywords.append(word) for word in adjKeywords if not (" " not in word and zipf_frequency(word, 'en') > 5)]

    # Remove words with the same topics.
    topics = []
    adj3Keywords = []
    for word in adj2Keywords:
        try:
            if pytrends.suggestions(word)[0]['mid'] not in topics:
                adj3Keywords.append(word)
                topics.append(pytrends.suggestions(word)[0]['mid'])
        except IndexError:
            continue

    print(f"Complete word cloud:        {adjKeywords}")
    print(f"Removed common words:       {list(set(adjKeywords) - set(adj2Keywords))}")
    print(f"Removed repeat topic words: {list(set(adjKeywords) - set(adj3Keywords))}")
    print(adj3Keywords)
    print(len(adj3Keywords))

    return adj3Keywords

def getMegaTrendData(keyword, region, timeframe, interval, cutoff):
    return getTrendsData(getViralKeywords(keyword, region, timeframe, interval, cutoff), region, timeframe, True)

def getTimeframes(start, end, interval):
    #start and end are in YYYY-MM-DD format.
    #interval is an integer in days.
    #return a list of all of the intervals in [YYYY-MM-DD YYYY-MM-DD] between a start and end date

    intervals = []

    startYear = int(start[:4]); startMonth = int(start[5:7]); startDay = int(start[8:])

    while decimalTime(start) < decimalTime(end):
        tempDay = startDay + interval; tempYear = startYear; tempMonth = startMonth

        #Adjust the day and month
        if tempDay > 30 and startMonth != 2:
            tempDay = tempDay % 30
            tempMonth += 1
        elif tempDay > 28 and startMonth == 2:
            tempDay = tempDay % 28
            tempMonth += 1

        #Adjust the month and year
        if tempMonth > 12:
            tempYear += 1
            tempMonth = tempMonth % 12

        #add the new interval to intervals
        start = toDatetime(tempYear, tempMonth, tempDay)

        intervals.append(toDatetime(startYear, startMonth, startDay) + " " + start)

        startDay = tempDay; startMonth = tempMonth; startYear = tempYear

    return intervals


def decimalTime(time):
    #input in YYYY-MM-DD format
    #output in YYYY.XX format.
    return int(time[:4]) + int(time[5:7])/12 + int(time[8:])/365


def toDatetime(year, month, day):
    #input as integers, output as YYYY-MM-DD
    MM = "0" + str(month) if month < 10 else str(month)
    return str(year) + "-" + str(MM) + "-" + str(day)


def plotStackedHist(data, title, legendFlag):
    # INPUT: if legendFlag is TRUE: then REVERSE the legend
    #        else, write it normally

    plt.figure()


    # Get the colors for the data
    colors = getColors(data)

    # Plot the data
    data.plot.bar(stacked=True, color=colors, figsize=(10,7))

    # Choose a font size
    fontP = FontProperties()
    fontP.set_size('small')

    # Adjust and show the rest of the figure
    if legendFlag:
        plt.legend(reversed(plt.legend().legendHandles), reversed(data.columns), loc='upper right', prop=fontP)
    else:
        plt.legend(data.columns, loc='upper right', prop=fontP)

    plt.title(title)
    plt.xticks(rotation='horizontal')
    plt.show()


def plotLine(data, title):
    plt.figure()

    # Get the colors for the data
    colors = getColors(data)

    # Plot the data
    data.plot.line(color=colors)

    # Adjust and show the rest of the figure
    plt.legend(reversed(plt.legend().legendHandles), reversed(data.columns), loc='upper right')
    plt.title(title)
    plt.xticks(rotation='horizontal')
    plt.show()


def getColors(data):
    colors = []
    for column in data.columns:
        if column in college_colors:
            colors.append(college_colors[column])

    # Randomly pick colors generally for when there are not colleges
    while len(colors) < len(data.columns):
        colors.insert(0, np.random.rand(3, ))

    return colors




