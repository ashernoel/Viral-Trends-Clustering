import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
plt.figure()

virality = [16, 6, 12, 21, 25, 17, 22, 22, 45, 33, 30, 55, 37, 38, 33]
virality = [14, 3, 9, 16, 21, 16, 21, 17, 33, 24, 27, 46, 33, 29, 30] #800 cutoff
virality = [10, 2, 9, 12, 18, 10, 16, 14, 26, 20, 18, 37, 28, 23, 23] #1000 cutoff
virality = [6, 1, 6, 12, 18, 11, 14, 10, 26, 19, 13, 24, 24, 20, 21] #1200 cutoff
virality = [13, 7, 15, 26, 21, 28, 19, 18, 30, 21, 44, 60, 25, 37, 39] #1 week, 800 cutoff
virality2 = [7, 1, 6, 13, 17, 11, 9, 12, 28, 21, 12, 31, 26, 25, 22]
subscribers = [6.9, 2.2, 3.4, 5.8, 5.3, 4.7, 5.0, 6.6, 8.3, 6.1, 6.1, 8.8, 9.6, 2.7, 6.8]
difference = [0.5, -0.8, 0.9, 1.3, -1, 1, 0.4, 1.5, 0.6, -0.6, 0.9, 1.2, 0.7, -2.3, -0.2]
plt.xlabel('Number of Viral Google Trends Topics')
plt.ylabel('Global Net Adds')
plt.title('Predicting Netflix Subscriber Adds')

plt.scatter(virality[0:4], subscribers[0:4], c='g', label='2016')
plt.scatter(virality[4:8], subscribers[4:8], c='r', label='2017')
plt.scatter(virality[8:12], subscribers[8:12], c='b', label='2018')
plt.scatter(virality[12:], subscribers[12:], c='y', label='2019')
plt.legend(loc='upper left')
plt.show()

# plt.scatter(wordfreqvirality, difference, c='r', label='data')
#
# plt.xlabel('Number of Viral Google Trends Topics')
# plt.ylabel('Difference between forecast and actual Net Adds')
# plt.title('Predicting Netflix Subscriber Adds')
# plt.show()

vpd = pd.DataFrame(virality, columns=["viral"])
sub = pd.DataFrame(subscribers, columns=["subs"])

xTrain, xTest, yTrain, yTest = train_test_split(vpd, sub, test_size = 1/3, random_state = 0)
linearRegressor = LinearRegression()
linearRegressor.fit(vpd, sub)

plt.scatter(vpd, sub, color = 'red')
plt.plot(vpd, linearRegressor.predict(vpd), color = 'blue')
print(r2_score(vpd, sub))

plt.show()