from googleTrendsUpgrade import *
from kmeansWordsAlgorithm import *
from googleSearchScraper import *
from collegeData import *




# INPUTS:
numberOfClusters = 9
dictionaryDepth = 3
input = {
    'query': "Massachusetts Institute of Technology",
    'region': metros["Boston"],
    'interval': '2018-01-01 2019-10-30',
    'cutoff': 1500,
}
outputName = "-".join([input['query'], input['region'], input['interval'], str(15), str(input['cutoff']), "1"])


viralKeywordList = getViralKeywords(input['query'], input['region'], input['interval'], 15, input['cutoff'])
print(viralKeywordList)

clusterKeywords = clusterSentencesSemantically(get_google_definitions(viralKeywordList, dictionaryDepth), numberOfClusters, outputName)

clusterSums = [0] * numberOfClusters
for index, row in clusterKeywords.iterrows():
    clusterSums[row["Cluster"]] += 1

print(clusterSums)
print(clusterKeywords)

plt.pie(clusterSums, labels=list(range(0, numberOfClusters)), colors=getColors(list(range(0, numberOfClusters))), startangle=90, autopct='%.1f%%')
plt.show()
