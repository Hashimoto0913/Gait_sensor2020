import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

num_of_cluster = 5 

#test_data = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\test.csv'

df = pd.read_csv('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\walkingdata.csv')

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

#クラスタ番号を追加
df['cluster_id'] = pred

#各クラスタの平均値
clusterinfo = pd.DataFrame()
for i in range(num_of_cluster):
    clusterinfo['cluster' + str(i)] = df[df['cluster_id'] == i].mean()
clusterinfo = clusterinfo.drop('cluster_id')
print(clusterinfo.T)

#train.csvの作成
df.to_csv('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\Train.csv')

#図として出力
fig, ax = plt.subplots(figsize=(12, 10))
my_plot = clusterinfo.T.plot(kind='bar', stacked=True, title="Mean Value of 4 Clusters",ax=ax)
my_plot.set_xticklabels(my_plot.xaxis.get_majorticklabels(), rotation=0)
#図を保存
plt.savefig('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\cluster_classification_diagram.png')
plt.show()
plt.close('all')