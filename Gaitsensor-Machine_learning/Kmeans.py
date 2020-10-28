import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

num_of_cluster = 13

test_data = 'D:\ドキュメント\KIT\専門ゼミ\python_code\stairs_test.csv'

df = pd.read_csv('D:\ドキュメント\KIT\専門ゼミ\python_code\walkingdata.csv')
#df = pd.read_csv(test_data)

array = np.array([df['bothfoot_L'].tolist(),
                  df['swing_L'].tolist(),
                  df['bothfoot_R'].tolist(),
                  df['swing_R'].tolist(),
                  df['stand_L'].tolist(),
                  df['stand_R'].tolist(),
                  ], np.int32)
array = array.T
pred = KMeans(n_clusters = num_of_cluster).fit_predict(array)

df['cluster_id'] = pred
clusterinfo = pd.DataFrame()
for i in range(num_of_cluster):
    clusterinfo['cluster' + str(i)] = df[df['cluster_id'] == i].mean()
clusterinfo = clusterinfo.drop('cluster_id')
print(clusterinfo)

#train.csvの作成
df.to_csv('D:\ドキュメント\KIT\専門ゼミ\python_code\Train.csv')

#図として出力
fig, ax = plt.subplots(figsize=(12, 10))
my_plot = clusterinfo.T.plot(kind='bar', stacked=True, title="Mean Value of 4 Clusters",ax=ax)
my_plot.set_xticklabels(my_plot.xaxis.get_majorticklabels(), rotation=0)
plt.show()