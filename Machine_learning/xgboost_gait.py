import xgboost as xgb
from xgboost import XGBClassifier
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# クラスタ数
num_of_cluster = 5
# 教師データ
train_data = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\Train(hashimoto).csv'
# モデルの保存先
classifier = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\classifier(hashimoto).pickle'

# pandasのDataFrameを作成
df = pd.read_csv(train_data)
data = pd.DataFrame(df, columns=['bothfoot_L','swing_L','bothfoot_R','swing_R','stand_L','stand_R'])
target = pd.DataFrame(df, columns=['cluster_id'])

# 訓練データとテストデータの取得
train_x, test_x, train_y, test_y = train_test_split(data, target, test_size=0.2, shuffle=True)
# 学習用データの一部を検証用データとして使用
train_x, valid_x, train_y, valid_y = train_test_split(train_x, train_y, test_size=0.2, shuffle=True)

# xgboost用の型に変換する
dtrain = xgb.DMatrix(train_x, label=train_y)  
dvalid = xgb.DMatrix(valid_x, label=valid_y)

# パラメータの設定　{'max_depth':"木の最大深度",'eta':"学習率",'objective':"学習目的",'num_class':"クラス数"}
# 検定を行う場合には'eval_metric'をパラメータに追加する　mlogloss = マルチクラスログロス 目的関数
param = {'max_depth': 2, 'eta': 0.5, 'objective': 'multi:softmax', 'num_class': num_of_cluster, 'eval_metric': 'mlogloss'}

# 学習
evallist = [(dvalid, 'eval'), (dtrain, 'train')]
num_round = 10000
bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=5) # 5回連続して評価指標が改善しなかったら学習を中断

# 検証結果の確認
print('Best Score:{0:.4f}, Iteratin:{1:d}, Ntree_Limit:{2:d}'.format(bst.best_score, bst.best_iteration, bst.best_ntree_limit))

### モデルの保存
learningmodel = XGBClassifier()
# pickle
with open(classifier, mode='wb') as f:
    pickle.dump(bst, f)
# xgb
# bst.save_model('./classifier.model')

# 検証結果のうち最も結果が良かったモデルで予測
dtest = xgb.DMatrix(test_x)
pred = ypred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)

# 精度の確認
score = accuracy_score(test_y, pred)
print('score:{0:.4f}'.format(score))