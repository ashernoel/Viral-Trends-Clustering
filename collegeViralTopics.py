from googleTrendsUpgrade import *

bostonMetro = 'US-NH-506'
sanfranMetro = 'US-CA-807'
searchMegaData = getMegaTrendData("Netflix", "", '2016-01-01 2019-10-30', 15, 800)

plotStackedHist(searchMegaData, "Netflix University", False)
plotStackedHist(searchMegaData.iloc[:, 1:], "Netflix More", True)