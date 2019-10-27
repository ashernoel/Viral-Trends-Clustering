# hello geena!
# hi asherrrrr

# Pytrends documentation: https://pypi.org/project/pytrends/
# Connect Pytrends API to google
from pytrends.request import TrendReq
import pandas as pd

# Remove the old hyper files from the last run time. Comment
import os
try:
    os.remove("outputData/annualUS.hyper")
    os.remove('outputData/annualAverage.hyper')
    os.remove('outputData/ivyWorld.hyper')
    os.remove('outputData/ivyUS.hyper')
except FileNotFoundError:
    print("Could not delete old .hyper files")

# https://pypi.org/project/pandleau/
from pandleau import *

def main():
    # Connect with Google somehow
    pytrends = TrendReq(hl='en-US', tz=360)

    # Define keywords to get data for
    colleges_HYPSM = [pytrends.suggestions('Harvard University')[0]['mid'],
                      pytrends.suggestions('Stanford University')[0]['mid'],
                      pytrends.suggestions('Massachusetts Institute of Technology')[0]['mid'],
                      pytrends.suggestions('Princeton University')[0]['mid'],
                      pytrends.suggestions('Yale University')[0]['mid']]

    colleges_usNews = ["Harvard University", "Princeton University", "Columbia University",
                       "Massachusetts Institute of Technology", "Yale University", "Stanford University",
                       "University of Chicago", "University of Pennsylvania"]

    colleges_ivyLeague1 = [pytrends.suggestions('Harvard University')[0]['mid'],
                           pytrends.suggestions("Brown University")[0]['mid'],
                           pytrends.suggestions("Columbia University")[0]['mid'],
                           pytrends.suggestions("Dartmouth College")[0]['mid']]

    colleges_ivyLeague2 = [pytrends.suggestions('Harvard University')[0]['mid'],
                           pytrends.suggestions("University of Pennsylvania")[0]['mid'],
                           pytrends.suggestions("Princeton University")[0]['mid'],
                           pytrends.suggestions("Yale University")[0]['mid'],
                           pytrends.suggestions("Cornell University")[0]['mid']
                           ]



    colleges_THERankings = ["University of Oxford", "California Institute of Technology",
                            "Cambridge University", "Stanford University", "Massachusetts Institute of Technology",
                            "Princeton University", "Harvard University", "Yale University", "University of Chicago",
                            "Imperial College London"]

    # HYPSM Dataframe: International and Domestic
    pytrends.build_payload(colleges_HYPSM, cat=0, timeframe='today 5-y', geo='', gprop='')
    worldData = pytrends.interest_over_time()
    print(worldData)
    pytrends.build_payload(colleges_HYPSM, cat=0, timeframe='today 5-y', geo='US', gprop='')
    usData = pytrends.interest_over_time()
    print(usData)
    worldData.columns = usData.columns = ["Harvard University", 'Stanford University',
                                          'Massachusetts Institute of Technology', 'Princeton University',
                                          'Yale University', "Useless Bool"]

    #IvyLeague Data Frame: International and Domestic

    pytrends.build_payload(colleges_ivyLeague1, cat=0, timeframe='today 5-y', geo='', gprop='')
    ivyWorld1 = pytrends.interest_over_time()
    pytrends.build_payload(colleges_ivyLeague2, cat=0, timeframe='today 5-y', geo='', gprop='')
    ivyWorld2 = pytrends.interest_over_time()
    ivyWorld = ivyWorld1.iloc[:, :-1].join(ivyWorld2.iloc[:, 1:-1])

    pytrends.build_payload(colleges_ivyLeague1, geo='US', cat=0, timeframe='today 5-y', gprop='')
    ivyUS1 = pytrends.interest_over_time()

    pytrends.build_payload(colleges_ivyLeague2, cat=0, timeframe='today 5-y', geo='US', gprop='')
    ivyUS2 = pytrends.interest_over_time()

    ivyUS = ivyUS1.iloc[:, :-1].join(ivyUS2.iloc[:, 1:-1])

    ivyWorld.columns = ["Harvard University", "Brown University", "Columbia University",
                                        "Dartmouth College", "University of Pennsylvania", "Princeton University",
                                        "Yale University", "Cornell University"]

    ivyUS.columns = ["Harvard University", "Brown University", "Columbia University",
                     "Dartmouth College", "University of Pennsylvania", "Princeton University",
                     "Yale University", "Cornell University"]

    # Rename the columns so they in english again in the same order as the original list
    annualWorld = getAnnualAverages(worldData, 5, 2014)
    annualUS = getAnnualAverages(usData, 5, 2014)
    ivyWorldOut = getAnnualAverages(ivyWorld, 5, 2014)
    ivyUSOut = getAnnualAverages(ivyUS, 5, 2014)

    outputData(annualWorld, 'outputData/annualWorld.hyper')
    outputData(annualUS, 'outputData/annualUS.hyper')
    outputData(ivyWorldOut, 'outputData/ivyWorld.hyper')
    outputData(ivyUSOut, 'outputData/ivyUS.hyper')

    #Print all the data for our article!
    print(worldData.mean())
    print(annualWorld.mean())
    print(usData.mean())
    print(annualUS.mean())

    print(ivyWorld.mean())
    print(ivyUS.mean())



    cleanDirectory()

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

# Create output tableau files in "outputData" folder
def outputData(data, name):
    data = pandleau(data)
    data.to_tableau(name, add_index=True)

# Delete the DataExtract files that get created for some reason
def cleanDirectory():
    directory = os.getcwd()
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            os.remove(filename)

main()




