import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# クラスタ数
num_of_cluster = 9

# 元データ
test_data = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\walkingdata\\walkingdata.csv'
# 教師データの保存先
train_data = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\Train.csv'
# クラスタごとの特徴図の保存先
pltfig = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\cluster_classification_diagram.png'

df = pd.read_csv(test_data)
array = np.array([df['bothfoot_L'].tolist(),
                  df['swing_L'].tolist(),
                  df['bothfoot_R'].tolist(),
                  df['swing_R'].tolist(),
                  df['stand_L'].tolist(),
                  df['stand_R'].tolist(),
                  ], np.int32)
array = array.T
# K-means法でクラスタリング
pred = KMeans(n_clusters = num_of_cluster).fit_predict(array)

# クラスタ番号にカラム名を追加
df['cluster_id'] = pred
# csv形式教師データの作成
df.to_csv(train_data)

# 各クラスタの平均値を計算
clusterinfo = pd.DataFrame()
for i in range(num_of_cluster):
    clusterinfo['cluster' + str(i)] = df[df['cluster_id'] == i].mean()
clusterinfo = clusterinfo.drop('cluster_id')
print(clusterinfo.T) # 各クラスタの平均値を表示

### クラスタごとの特徴を図として出力
fig, ax = plt.subplots(figsize=(12, 10))
my_plot = clusterinfo.T.plot(kind='barh', stacked=True, title="Mean Value of 4 Clusters",ax=ax)
# 図を保存
plt.savefig(pltfig)
plt.show()
plt.close('all')