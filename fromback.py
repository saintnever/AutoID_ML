import threading
import re
import socket
import time
from datetime import datetime, timedelta
import pandas as pd
from button_bitid import Button

xInput = {}
xInput['EPC']=[]
xInput['Antenna'] = []
xInput['Freq']=[]
xInput['ReaderTimestamp']=[]
xInput['RSSI']=[]
xInput['Doppler']=[]
xInput['Phase']=[]
xInput['ComputerTimestamp']=[]
index = 0
button = Button('E2000019390701021310458F')
def receivedata():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('192.168.53.131',14))
    first_number = ''
    while True:
        data = s.recv(2048).decode()
        # print(data)
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
                global xInput
                if item == '':
                    continue
                else:
                    if k  ==  1:
                        xInput['EPC'].append(item)
                    elif k == 2:
                        xInput['Antenna'].append(int(item))
                    elif k == 3:
                        xInput['Freq'].append(float(item))
                    elif k == 4:
                        xInput['ReaderTimestamp'].append(timedelta(seconds = (float(item)/1000)))
                    elif k == 5:
                        xInput['RSSI'].append(float(item))
                    elif k == 6:
                        xInput['Doppler'].append(float(item))
                    elif k == 7:
                        xInput['Phase'].append(float(item))
                    elif k == 8:
                        xInput['ComputerTimestamp'].append(timedelta(seconds = (float(item[:-1])/1000)))
                    i += 1
        else:
            break
        # print(xInput)

def lower_bound(array,first,last,value):
    while first < last:
        mid =  first + (last - first) // 2
        if array[mid] <  value:first = mid  + 1
        else: 
            last = mid
    return first

def processdata():
    global xInput
    global index
    timeEnd = timedelta(seconds = 0)
    win = timedelta(seconds=0.1)
    step = timedelta(seconds=0.05)
    while True:
        if len(xInput['ReaderTimestamp']):
            while True:
                temp = max(xInput['ReaderTimestamp'])
                # 考虑两个时间节点，一个是按照step走的timeEnd，还有一个是现在接收到的数据的最迟时间
                if  temp > timeEnd:
                    timeEnd = temp
                    break
                else:
                    time.sleep(0.1)
            timeStart = timeEnd - win
            index  = lower_bound(xInput['ReaderTimestamp'],index,len(xInput['ReaderTimestamp']),timeStart)
            print(button.winstatusChangelist(xInput,index))
            timeEnd = timeEnd+step

# receivedata()

t1 = threading.Thread(target=receivedata, args=())
t2 = threading.Thread(target=processdata, args=())
t1.start()
t2.start()
# t1.join()
# t2.join()




