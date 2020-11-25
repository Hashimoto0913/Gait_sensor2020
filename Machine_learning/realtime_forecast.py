import serial
import csv
import xgboost as xgb
import numpy as np
import pandas as pd
import pickle

#保存するファイル
test_data = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\walkingdata\\walkingdata(hashimoto).csv'
classifier = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\Machine_learning\\classifier(hashimoto).pickle'
bst = pickle.load(open(classifier, 'rb'))
ser = serial.Serial('COM5', baudrate=115200, parity=serial.PARITY_NONE)
line = ser.readline()
total_byte = 0
try:
    #追記
    while True:
        line = ser.readline()
        total_byte = total_byte + len(line.decode('utf-8'))
        print("                                 byte:",len(line.decode('utf-8'))," total_byte:", total_byte)
        line_str = (line.decode('utf-8')).replace('\n', '') #byteをstrに変換後、改行コードを削除
        lines = line_str.split(',')
        print(lines)
        with open(test_data, 'a',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(lines)
        # pandasのDataFrameを作成
        df = pd.read_csv(test_data)
        data = pd.DataFrame(df, columns=['bothfoot_L','swing_L','bothfoot_R','swing_R','stand_L','stand_R'])
        #最終行を対象に予測
        dtest = xgb.DMatrix(data.tail(1))
        pred = ypred = bst.predict(dtest, ntree_limit=bst.best_ntree_limit)
        print(pred[0])
        cpred = int(pred[0])
        if cpred == 0:
            print("tried")
        elif cpred == 1:
            print("normal")
        elif cpred == 2:
            print("stop")
        else:
            print("run")
except KeyboardInterrupt:
    #確認用
    with open(test_data) as f:
        print(f.read())

    ser.close()