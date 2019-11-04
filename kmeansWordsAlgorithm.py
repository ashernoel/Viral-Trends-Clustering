from googleSearchScraper import *

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import glob
from sklearn.cluster import KMeans
import os.path

def clusterSentencesSemantically(data, number_of_clusters, output_name):




    vec = TfidfVectorizer(stop_words="english",
                          max_df=0.75,
                          min_df=0.01,
                          max_features=1000000,
                          use_idf=True)

    # Fit from the 'descriptions' column of our dataframe
    matrix = vec.fit_transform(data['Descriptions'])

    # Then turn it into a new dataframe
    results = pd.DataFrame(matrix.toarray(), columns=vec.get_feature_names())

    print(results)
    print(results.head)

    km = KMeans(n_clusters=number_of_clusters)

    print("Fitting", number_of_clusters, "clusters using a ", matrix.shape, "matrix")

    # Let's fit it!
    km.fit(matrix)

    print("Top terms per cluster:")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vec.get_feature_names()
    for i in range(number_of_clusters):
        top_ten_words = [terms[ind] for ind in order_centroids[i, :30]]
        print("Cluster {}: {}".format(i, ' '.join(top_ten_words)))


    data['Cluster'] = km.labels_

    while os.path.exists(f'{output_name}.csv'):
        output_name = output_name.rsplit("-", 1)[0] + "-" + str(int(output_name.split("-")[-1]) + 1)

    data[["Keywords", "Cluster"]].to_csv(f'{output_name}.csv', index=None, header=True)

    return data
