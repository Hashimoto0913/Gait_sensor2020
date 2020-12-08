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
### 5.realtime_forecast.py  
* 使用ライブラリ：serial,csv,pandas,numpy,pickle,xgboost
* *1. gait_forecast.py*に予測機能をつけたもの
* 「classfiler.pickle」から呼び出した学習モデルを使用し、送られてきた歩行データに対して予測を行う
* PC側のターミナルに予測して得られたクラスタ番号を表示する
* 送られてきたデータは「walkingdata.csv」に保存される
