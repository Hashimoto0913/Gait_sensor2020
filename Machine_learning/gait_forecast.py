import xgboost as xgb
import numpy as np
import pandas as pd
import pickle
import csv

# 予測対象の歩行データ
testdata = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\walkingdata\\walkingdata.csv'
# 使用する学習モデル
classifier = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\classifier.pickle'
# 結果の出力先
result = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\prediction_result.csv'

# pandasのDataFrameを作成
df = pd.read_csv(testdata)
data = pd.DataFrame(df, columns=['bothfoot_L','swing_L','bothfoot_R','swing_R','stand_L','stand_R'])

# 学習済みモデルを読み込み、予測を行う(長期予測)
bst = pickle.load(open(classifier, 'rb'))
dtest = xgb.DMatrix(data)
pred = ypred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)

# クラスタ番号を追加したものを書き出し
df['cluster_id'] = pred
# クラスタ番号から歩行の状態を書き出し
df['result'] = pred
df.result = df.result.replace(0, "Run")
df.result = df.result.replace(4, "Tired")
df.result = df.result.replace(3, "Normal")
df.result = df.result.replace(2, "Stop")
df.result = df.result.replace(1, "Stop")
#結果を出力
df.to_csv(result)

'''
# 精度の計算 Train.csvの元のデータからprediction_result.csvを作成した場合のみ可能
# 新規のデータは正解ラベルが存在しないため精度がわからない

df_train = pd.read_csv('C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\Train.csv')
df_result = pd.read_csv(result)
origin = pd.DataFrame(df_train, columns=['cluster_id'])
result = pd.DataFrame(df_result, columns=['cluster_id'])

# 全体数
n = len(origin)
print("Number of data:",n)
# 誤認識数
k = origin[~origin.isin(result.to_dict(orient='list')).all(1)]
print("Incorrect answer:",len(k))
if len(k) != 0: print(k,"\n")

# 精度
print("accuracy:" , round(1 - len(k)/n,4))　# 小数点４桁まで表示
'''