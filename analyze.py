# Pytrends documentation: https://pypi.org/project/pytrends/
# Connect Pytrends API to google
from pytrends.request import TrendReq
import pandas as pd

import matplotlib.pyplot as plt

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
                  "University of Pennsylvania": "tab:purple"
                  }


def main():

    # Define keywords to get data for
    colleges_HYPSM = ["Harvard University", 'Stanford University',
                      'Massachusetts Institute of Technology', 'Princeton University',
                      'Yale University']

    colleges_ivyLeague = ["Harvard University", "Brown University", "Columbia University",
                          "Dartmouth College", "University of Pennsylvania", "Princeton University",
                          "Yale University", "Cornell University"]

    ivyUS = getTrendsData(colleges_ivyLeague, 'US', 'today 5-y', True)


    # Rename the columns so they in english again in the same order as the original list
    ivyUSOut = getAnnualAverages(ivyUS, 5, 2015)

    print(ivyUSOut.mean())

    plotLine(ivyUSOut.iloc[:, ::-1], "Domestic Ivy League Search Data Over Time")

    plotStackedHist(ivyUSOut.iloc[:, ::-1], "Domestic Ivy League Search Data Over Time")

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

    # Initialize flag and temporary list of quieries with the keyword that should be in all of them.
    old = 0
    tempList = [pytrends.suggestions(keywords[0])[0]['mid']] if flagTopic else [keywords[0]]

    # Initialize the datastructures
    trendData = pd.DataFrame()
    oldData = pd.DataFrame()

    for index in range(1, len(keywords)):

        # Add the next keyword in the list to the temporary list of queries
        keyword = keywords[index]

        tempList.append(pytrends.suggestions(keyword)[0]['mid']) if flagTopic else tempList.append(keyword)

        # The maximum query request is five terms
        if index // 4 != old or (index == len(keywords) - 1):

            # Build the payload
            pytrends.build_payload(tempList, cat=0, timeframe=timeframe, geo=region, gprop='')
            newData = pytrends.interest_over_time()

            # Merge the old and new DataFrames
            if old == 0:
                oldData = newData.iloc[:, :-1]
                trendData = oldData
            else:
                trendData = oldData.join(newData.iloc[:, 1:-1])

            # Reset the temporary queries and increase the flag.
            tempList = [pytrends.suggestions(keywords[0])[0]['mid']] if flagTopic else [keywords[0]]
            old += 1

    # Update the columns of the trend data with the original names
    trendData.columns = keywords

    # Reorder the columns based off of their mean values.
    return trendData.reindex(trendData.mean().sort_values(ascending=False).index, axis=1)

def plotStackedHist(data, title):
    plt.figure()

    # Get the colors for the colleges
    colors = []
    for column in data.columns:
        colors.append(college_colors[column])

    # Plot the data
    data.plot.bar(stacked=True, color=colors, figsize=(10,7))

    # Adjust and show the rest of the figure
    plt.legend(reversed(plt.legend().legendHandles), reversed(data.columns), loc='upper right')
    plt.title(title)
    plt.xticks(rotation='horizontal')
    plt.show()


def plotLine(data, title):
    plt.figure()

    # Get the colors for the colleges
    colors = []
    for column in data.columns:
        colors.append(college_colors[column])

    # Plot the data
    data.plot.line(color=colors)

    # Adjust and show the rest of the figure
    plt.legend(reversed(plt.legend().legendHandles), reversed(data.columns), loc='upper right')
    plt.title(title)
    plt.xticks(rotation='horizontal')
    plt.show()

main()




