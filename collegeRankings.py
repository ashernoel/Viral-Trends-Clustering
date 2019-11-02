from googleTrendsUpgrade import *

colleges_HYPSM = ["Harvard University", 'Stanford University',
                      'Massachusetts Institute of Technology', 'Princeton University',
                      'Yale University']

colleges_ivyLeague = ["Harvard University", "Brown University", "Columbia University",
                      "Dartmouth College", "University of Pennsylvania", "Princeton University",
                      "Yale University", "Cornell University", "Northeastern University"]

ivyUS = getTrendsData(colleges_ivyLeague, 'US', 'today 5-y', True)

# Rename the columns so they in english again in the same order as the original list
ivyUSOut = getAnnualAverages(ivyUS, 5, 2015)


plotLine(ivyUSOut.iloc[:, ::-1], "Domestic Ivy League Search Data Over Time")
plotStackedHist(ivyUSOut.iloc[:, ::-1], "Domestic Ivy League Search Data Over Time")