import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import csv

#対象のデータ
testdata = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\walkingdata.csv'

header = "cluster_id"
headers = header.split(',')

# pandasのDataFrameを作成
df = pd.read_csv(testdata)
data = pd.DataFrame(df, columns=['bothfoot_L','swing_L','bothfoot_R','swing_R','stand_L','stand_R'])

#学習済みモデルを読み込み、予測を行う(長期予測)
bst = pickle.load(open('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\classifier.pickle', 'rb'))

dtest = xgb.DMatrix(data)
pred = ypred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
l_pred = pred.tolist()
#クラスタ番号を追加したものを書き出し
df[header] = pred
#クラスタ番号から歩行の状態を書き出し
df['result'] = pred
df.result = df.result.replace(0, "Run")
df.result = df.result.replace(1, "Tired")
df.result = df.result.replace(2, "Normal")
df.result = df.result.replace(3, "Stop(R)")
df.result = df.result.replace(4, "Stop(L)")

#結果を出力
df.to_csv('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\prediction_result.csv')

'''
#精度の計算 Train.csvの元のデータからprediction_result.csvを作成した場合のみ可能
#新規のデータは正解ラベルが存在しないため精度がわからない

df_train = pd.read_csv('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\Train.csv')
df_result = pd.read_csv('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\prediction_result.csv')
origin = pd.DataFrame(df_train, columns=['cluster_id'])
result = pd.DataFrame(df_result, columns=['cluster_id'])

#全体数
n = len(origin)
print("Number of data:",n)
#誤認識数
k = origin[~origin.isin(result.to_dict(orient='list')).all(1)]
print("Incorrect answer:",len(k))
if len(k) != 0: print(k,"\n")

#精度
print("accuracy:" , round(1 - len(k)/n,4))
'''