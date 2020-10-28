import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import csv

header = "cluster_id,"
headers = header.split(',')

# pandasのDataFrameを作成
df = pd.read_csv('D:\ドキュメント\KIT\専門ゼミ\python_code\walkingdata.csv')
data = pd.DataFrame(df, columns=['bothfoot_L','swing_L','bothfoot_R','swing_R','stand_L','stand_R'])

#学習済みモデルを読み込み、予測を行う(長期予測)
bst = pickle.load(open('classifier.pickle', 'rb'))

dtest = xgb.DMatrix(data)
pred = ypred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
l_pred = pred.tolist()

#初期化
with open('D:\\ドキュメント\\KIT\\専門ゼミ\\python_code\\prediction_result.csv', 'w',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

with open('D:\\ドキュメント\\KIT\\専門ゼミ\\python_code\\prediction_result.csv', 'a',newline="") as f:
    writer = csv.writer(f)
    for ele in l_pred:
        writer.writerow([ele])

#精度の計算
df_train = pd.read_csv('D:\ドキュメント\KIT\専門ゼミ\python_code\Train.csv')
df_result = pd.read_csv('D:\ドキュメント\KIT\専門ゼミ\python_code\prediction_result.csv')

origin = pd.DataFrame(df_train, columns=['cluster_id'])
result = pd.DataFrame(df_result, columns=['cluster_id'])

#全体数
n = len(origin)
print("Number of data:",n)
#誤認識数
k = len(origin[~origin.isin(result.to_dict(orient='list')).all(1)])
print("Incorrect answer:",k)
print(origin[~origin.isin(result.to_dict(orient='list')).all(1)],"\n")

#精度
print("accuracy:" , round(1 - k/n,4))