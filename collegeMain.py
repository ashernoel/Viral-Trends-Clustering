from googleTrendsUpgrade import *
from kmeansWordsAlgorithm import *
from googleSearchScraper import *
from collegeData import *


def get_pie_topics(keyword, region, interval, cutoff, number_of_clusters, dictionary_depth):


    # INPUTS:
    input = {
        'query': keyword,
        'region': region,
        'interval': interval,
        'cutoff': cutoff,
    }
    outputName = "-".join([input['query'], input['region'], input['interval'], str(15), str(input['cutoff']), "1"])


    viralKeywordList = getViralKeywords(input['query'], input['region'], input['interval'], 15, input['cutoff'])
    print(viralKeywordList)

    clusterKeywords = clusterSentencesSemantically(get_google_definitions(viralKeywordList, dictionary_depth), number_of_clusters, outputName)

    clusterSums = [0] * number_of_clusters
    for index, row in clusterKeywords.iterrows():
        clusterSums[row["Cluster"]] += 1

    print(clusterSums)
    print(clusterKeywords)

    plt.title(keyword + ": Related Search Categories in " + list(metros.keys())[list(metros.values()).index(region)])

    plt.pie(clusterSums, labels=list(range(0, number_of_clusters)), colors=getColors(list(range(0, number_of_clusters))), startangle=90, autopct='%.1f%%')
    plt.show()


# DATA has been collected. This is now unnecessary.
# for i in range(21, 30):
#     numClusters = 7
#     if i % 2 == 0:
#         numClusters = 8
#     if i % 3 == 0:
#         numClusters = 6
#
#     query = "Massachusetts Institute of Technology"
#     region = metros["Boston"]
#
#     if i > 20:
#         query = "Stanford University"
#         region = metros["San Fran"]
#     elif i > 10:
#         query = "Harvard University"
#
#     get_pie_topics(query, region, "2018-01-01 2019-11-01", 2000, numClusters, 3)