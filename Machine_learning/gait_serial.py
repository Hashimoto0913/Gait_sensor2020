#タイムスタンプとバイト数　一歩分の周期　周波数
import serial
import csv

#保存するファイル
test_data = 'C:\\Users\\user\\Documents\\Gaitsensor-main\\walkingdata\\walkingdata(hashimoto).csv'

ser = serial.Serial('COM5', baudrate=115200, parity=serial.PARITY_NONE)

header = "bothfoot_L,swing_L,bothfoot_R,swing_R,stand_L,stand_R"
headers = header.split(',')
line = ser.readline()

total_byte = 0


'''
#初期化
with open(test_data, 'w',newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
'''
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

except KeyboardInterrupt:
    #確認用
    with open(test_data) as f:
        print(f.read())

    ser.close()