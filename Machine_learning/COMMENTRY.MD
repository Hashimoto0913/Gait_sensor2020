機械学習  
***
### 1.gait_serial.py  
* 使用ライブラリ：pyserial,csv
* 靴から送られてくる歩行1周期分のデータを「walkingdata.csv」に保存していく  
### 2.Kmeans.py  
* 使用ライブラリ：csv,pandas,numpy,matplot,scikit-learn
* 「walkingdata.csv」をKmeans法でクラスタリング
* 「walkingdata.csv」にクラスタ番号を付与したものを「Train.csv」として保存
* 各クラスタの特徴をプロットして表示し、クラスタ番号ごとに状態を定義する
* プロットされた結果は「cluster_classification_diagram.png」として保存
### 3.xgboost_gait.py  
* 使用ライブラリ：xgboost,pandas,pickle,scikit-learn
* 「Train.csv」を教師データとし、学習を行う
* 学習の結果最も精度が良いモデルをpickleを使い「classfiler.pickle」として保存
* 念のためxgboostのメソッドを使用した方法でも保存している
### 4.gait_forecast.py  
* 使用ライブラリ：csv,pandas,numpy,pickle,xgboost
* 「classfiler.pickle」から呼び出した学習モデルを使用し、歩行データに対して予測を行う
* 予測して得られたクラスタ番号とその状態の説明を元の歩行データに追加し、「prediction_result.csv」として保存　　
#### 「クラスタ分類図.png」  
* 2020/11/09時点で検証に使用しているクラスタの図  
cluster_0:Run,走っている  
cluster_1:Tired,疲れている  
cluster_2:Normal,平常  
cluster_3:Stop(R),停止(右足から)  
cluster_4:Stop(L),停止(左足から)  
