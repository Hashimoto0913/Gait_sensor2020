import xgboost as xgb
import numpy as np
import pandas as pd
import pickle
import csv
import matplotlib.pyplot as plt
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

#折れ線グラフで歩行状態の遷移を確認
df['score'] = df['result']
df.score = df.score.replace("Run", 4.5)
df.score = df.score.replace("Tired",0.8)
df.score = df.score.replace("Normal",1.25)
df.score = df.score.replace("Stop(R)",0)
df.score = df.score.replace("Stop(L)",0)

#n歩ごとの平均
steps= 15
fix = 0 
ave_move = []
list_score = df.score.tolist()
#割り切れない場合は割り切れる歩数までを計算する
if len(list_score)%steps != 0: 
    fix = len(list_score) % steps
for i in range(0,len(list_score)-fix,steps):
    sm = 0
    for j in range(i,i+steps):
        sm = sm + list_score[j]
    ave_move.append(sm/steps)
plt.plot(ave_move)
plt.show()

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