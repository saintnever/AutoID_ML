import threading
import re
import socket
import time
from datetime import datetime, timedelta
import pandas as pd
from button_bitid import Button
import csv
from collections import deque

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
    __clickResultdic={}
    __interactionflag = False
    __clickflag = False

    # 存放interaction的上一个状态
    __lastresultdic={}
    __lastresultlist=[]


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
        self.epc_queue = deque()
        self.readerTimestamp_queue = deque()

    def detect_status(self, host, port,event,eventlist):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        first_number = ''
        curRSSI = -300
        curEPC = ''
        while True:
            if event.is_set():
                data = s.recv(2048).decode()
                writelist = []
                # print(data)
                if data:
                    # 处理不完整的信息
                    data = first_number + data
                    first_number = ''
                    while not data[-1:] == '\n':
                        first_number = data[-1:] + first_number
                        data = data[:-1]

                    datalist = re.split('[,;]', data)
                    # print(datalist)
                    i = 0
                    start_time = 0
                    pepc = 0
                    for item in datalist:
                        k = i % 9
                        if item == '':
                            continue
                        else:
                            if k == 1:
                                self.__xInput['EPC'].append(item)
                                self.epc_queue.append(item)
                                curEPC = item
                            elif k == 2:
                                self.__xInput['Antenna'].append(int(item))
                            elif k == 3:
                                self.__xInput['Freq'].append(float(item))
                            elif k == 4:
                                # ctime = timedelta(seconds=(float(item) / 1000))
                                ctime = float(item)
                                self.__sensingResultlist = []
                                self.__xInput['ReaderTimestamp'].append(ctime)
                                self.readerTimestamp_queue.append(ctime)
                                # pop all items outside the sliding window
                                while len(self.readerTimestamp_queue) > 0:
                                    ptime = self.readerTimestamp_queue.popleft()
                                    if ctime - ptime > 200:
                                        self.epc_queue.popleft()
                                    else:
                                        self.readerTimestamp_queue.appendleft(ptime)
                                        break
                                # print(list(self.readerTimestamp_queue), list(self.epc_queue))
                                for epc in self.__sensingEPClist:
                                    self.__sensingResultlist.append(bool(self.epc_queue.count(epc)))
                                self.__lastresultlist = self.__interactionResultlist
                                self.__interactionResultlist = []
                                for epc in self.__interactionEPClist:
                                    self.__interactionResultlist.append(bool(self.epc_queue.count(epc)))
                                # if len(self.__interactionResultlist) and len(self.__lastresultlist):
                                #     if not self.__interactionResultlist[0] == self.__lastresultlist[0]:
                                #         print(self.__interactionResultlist,self.__lastresultlist)
                                im = 0
                                self.__clickResultlist = []
                                for epc in self.__interactionEPClist:
                                    if self.__interactionResultlist[im]:
                                        if not self.__lastresultlist[im]:
                                            eventlist[im].set()
                                            self.__clickResultdic[epc] = "True"
                                        else:
                                            self.__clickResultdic[epc] = "False"
                                    else:
                                        self.__clickResultdic[epc] = "False"
                                    im += 1
                                # for item in self.__clickResultdic.values():
                                #     if item  == "True":
                                #         upevent.set()
                                #         print(self.__clickResultdic)
                                # upevent.set()

                            elif k == 5:
                                self.__xInput['RSSI'].append(float(item))
                                curRSSI = float(item)
                            elif k == 6:
                                self.__xInput['Doppler'].append(float(item))
                            elif k == 7:
                                self.__xInput['Phase'].append(float(item))
                            elif k == 8:
                                self.__xInput['ComputerTimestamp'].append(timedelta(seconds=(float(item[:-1]) / 1000)))
                            else:
                                self.updateEPC(curRSSI, curEPC)
                            i += 1
                else:
                    break
            else:
                s.close()
                break

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
        # length = len(self.__interactionEPClist)
        # while not (len(self.__interactionResultlist) == length):
        #     pass
        # return self.__interactionResultlist
        # while not self.__interactionflag:
            # i = 1
        # if self.__clickResultlist[0]  == "True":
        #     print(self.__clickResultlist)
        # print(self.__clickResultlist)
        # if self.__interactionflag:
        #     print("you can get data from me")
        return self.__clickResultdic

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
# example

if __name__ == '__main__':
    r_event = threading.Event()
    up_event = threading.Event()
    EPClist = ['E2000019390700211300052E']
    # 创建一个eventlist
    length = len(EPClist)
    eventlist = []
    for i in range(length):
        tempevent =  threading.Event()
        eventlist.append(tempevent)
    try:
        d = detection()
        t1 = threading.Thread(target=d.detect_status, args=('101.6.114.22',14,r_event,eventlist,))
        # t2 = threading.Thread(target=d.processdata, args=())
        t1.start()
        r_event.set()
        # t2.start()
        iiii = 0
        while True:
            # EPClist = ['E2000019390700191300052D','E20000193907001913100535']
            # d.updateSensingEPC(EPClist)
            d.updateInteractionEPC(EPClist)
            # result = d.getSensingresult()
            for event in eventlist:
                if event.is_set():
                    # 说明此时有点击事件
                    print("true",iiii)
                    event.clear()
                    iiii += 1
    except KeyboardInterrupt as e:
        print ("Exiting...")
    finally:
        r_event.clear()
        t1.join()
