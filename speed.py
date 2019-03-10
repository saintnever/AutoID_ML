import re
import socket
import time
from datetime import datetime, timedelta
import pandas as pd
from button_bitid import Button

df_data =pd.DataFrame(columns=('EPC','Antenna','Freq','ReaderTimestamp','RSSI','Doppler','Phase','ComputerTimestamp'))

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.53.131',14))
first_number = ''
timeStart = 0
timeEnd = 0
win = timedelta(seconds=0.5)
step = timedelta(seconds=0.1)
# 定义button
button = Button('E2000019390701021310458F')
while True:
    data = s.recv(2048).decode()
    if data:
        # 处理不完整的信息
        data = first_number + data
        first_number = ''
        while not  data[-1:] == '\n':
            first_number = data[-1:] + first_number
            data =  data[:-1]

        datalist = re.split('[,;]', data)
        i = 0
        for item in datalist:
            k = i % 9
            if item == '':
                continue
            else:
                if k  ==  1:
                    xInput = {}
                    xInput['EPC']=[item]
                elif k == 2:
                    xInput['Antenna']=[int(item)]
                elif k == 3:
                    xInput['Freq']=[float(item)]
                elif k == 4:
                    xInput['ReaderTimestamp']=[timedelta(seconds = (float(item)/1000))]
                elif k == 5:
                    xInput['RSSI']=[float(item)]
                elif k == 6:
                    xInput['Doppler']=[float(item)]
                elif k == 7:
                    xInput['Phase']=[float(item)]
                elif k == 8:
                    xInput['ComputerTimestamp']=[timedelta(seconds = (float(item[:-1])/1000))]
                    # xInput['ComputerTimestamp']=[float(item[:-1])]
                    df_data = df_data.append(pd.DataFrame(xInput),ignore_index=True)
                i += 1
    else:
        break
    if timeStart == 0:
        timeStart = df_data['ReaderTimestamp'].min()
        timeEnd =  timeStart + win
    df_exist = df_data[(df_data['ReaderTimestamp'] >= timeEnd)]
    if len(df_exist) > 0:
        df_frame = df_data[(df_data['ReaderTimestamp'] >= timeStart) & (df_data['ReaderTimestamp'] < timeEnd)]
        result = button.winstatusChange(df_frame)
        # print(result)
        timeStart = timeStart + step
        timeEnd =  timeStart + win
        df_data = df_data[(df_data['ReaderTimestamp'] >= timeStart)]
    print(df_data)
    print(time.time())
    break
s.close()