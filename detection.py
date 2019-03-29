import threading
import re
import socket
import time
from datetime import datetime, timedelta
import pandas as pd
from button_bitid import Button
import csv

class detection:
    __xInput = {}
    __index = 0

    # 存放sensingEPC
    __sensingEPClist=[]
    # 存放interactionEPC
    __interactionEPClist=[]

    # 存放结果 
    __sensingResultlist = []
    __interactionResultlist=[]

    # 存放interaction的上一个状态
    __lastresultdic={}


    def __init__(self):
        self.__xInput['EPC']=[]
        self.__xInput['Antenna'] = []
        self.__xInput['Freq']=[]
        self.__xInput['ReaderTimestamp']=[]
        self.__xInput['RSSI']=[]
        self.__xInput['Doppler']=[]
        self.__xInput['Phase']=[]
        self.__xInput['ComputerTimestamp']=[]
        self.maxRSSI = -300
        self.maxEPC = ''
        self.threshold = -100

    def receivedata(self, host, port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host, port))
        first_number = ''
        curRSSI = -300
        curEPC = ''
        while True:
            data = s.recv(2048).decode()
            writelist = []
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
                    if item == '':
                        continue
                    else:
                        if k  ==  1:
                            self.__xInput['EPC'].append(item)
                            curEPC = item
                        elif k == 2:
                            self.__xInput['Antenna'].append(int(item))
                        elif k == 3:
                            self.__xInput['Freq'].append(float(item))
                        elif k == 4:
                            self.__xInput['ReaderTimestamp'].append(timedelta(seconds = (float(item)/1000)))
                        elif k == 5:
                            self.__xInput['RSSI'].append(float(item))
                            curRSSI = float(item)
                        elif k == 6:
                            self.__xInput['Doppler'].append(float(item))
                        elif k == 7:
                            self.__xInput['Phase'].append(float(item))
                        elif k == 8:
                            self.__xInput['ComputerTimestamp'].append(timedelta(seconds = (float(item[:-1])/1000)))
                        else:
                            self.updateEPC(curRSSI, curEPC)
                        i += 1
            else:
                break

    def updateEPC(self, rssi, epc):
        if rssi > self.maxRSSI:
            self.maxRSSI = rssi
            self.maxEPC = epc

    def resetEPC(self):
        while True:
            self.maxRSSI = -300 
            self.maxEPC = ''
            time.sleep(1)

    def getTopTag(self):
        if self.maxRSSI > self.threshold:
            print('EPC info' +str(self.maxRSSI) +self.maxEPC)
            return self.maxEPC 
        else:
            return 'None' 

    def updateSensingEPC(self,xEPClist):
        # print(xEPClist)
        self.__sensingEPClist = xEPClist

    def updateInteractionEPC(self,xEPClist):
        self.__interactionEPClist = xEPClist

    def getSensingresult(self):
        return self.__sensingResultlist

    def getInteractionresult(self):
        return self.__interactionResultlist

    def lower_bound(self,array,first,last,value):
        while first < last:
            mid =  first + (last - first) // 2
            if array[mid] <  value:first = mid  + 1
            else: 
                last = mid
        return first

    def resetEPC(self):
        while True:
            self.maxRSSI = -300 
            self.maxEPC = ''
            time.sleep(1)

    def processdata(self):
        timeEnd = timedelta(seconds = 0)
        win = timedelta(seconds=0.2)
        step = timedelta(seconds=0.1)
        while True:
            if len(self.__xInput['ReaderTimestamp']):
                # print("~~~~~")
                # while True:
                timeEnd = max(self.__xInput['ReaderTimestamp'])
                # # 考虑两个时间节点，一个是按照step走的timeEnd，还有一个是现在接收到的数据的最迟时间
                #     if  temp > timeEnd:
                #         timeEnd = temp
                #         break
                #     else:
                #         time.sleep(0.1)
                    # timeEnd = temp
                timeStart = timeEnd - win
                self.__index  = self.lower_bound(self.__xInput['ReaderTimestamp'],self.__index,len(self.__xInput['ReaderTimestamp']),timeStart)
                buttonlist = []
                # 对sensing tag的状态做处理
                # print("*****")
                for item in self.__sensingEPClist:
                    tempbutton = Button(item)
                    buttonlist.append(tempbutton)
                    # result = tempbutton.winstatusChangelist(self.__xInput,self.__index)
                    # print(result)
                    # self.__sensingResultdic[item] = result
                self.__sensingResultlist = []
                for item in buttonlist:
                    self.__sensingResultlist.append(item.winstatusChangelist(self.__xInput,self.__index))
                # print(self.__sensingResultlist)
                # 对interaction tag的状态做处理
                buttonlist = []
                # 对interaction tag的状态做处理
                for item in self.__interactionEPClist:
                    tempbutton = Button(item)
                    buttonlist.append(tempbutton)
                tempresultdic = {}
                for item in buttonlist:
                    status = item.winstatusChangelist(self.__xInput,self.__index)
                    tempresult[item] = status
                    # 如果是新增进来的标签
                    if not item in self.__lastresultdic:
                        # 那么只考虑短路开关
                        if not status:
                            # true代表被按下
                            self.__interactionResultlist.append("true")
                        else:
                            self.__interactionResultlist.append("false")
                    else:
                        laststatus = self.__lastresultdic[item]
                        if not status:
                            if not laststatus:
                                self.__interactionResultlist.append("false")
                            else:
                                self.__interactionResultlist.append("true")
                        else:
                            self.__interactionResultlist.append("false")
                self.__lastresultdic = tempresultdic                   
            timeEnd = timeEnd+step

# example

if __name__ == '__main__':
    d = detection()
    t1 = threading.Thread(target=d.receivedata, args=('101.6.114.22', 14))
    t2 = threading.Thread(target=d.processdata, args=())
    t1.start()
    t2.start()
    while True:
        EPClist = ['E2000019390700191300052D']
        d.updateSensingEPC(EPClist)
        result = d.getSensingresult()
        print(result)
        time.sleep(0.5)
