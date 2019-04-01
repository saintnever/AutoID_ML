import threading
import re
import socket
import time
from datetime import datetime, timedelta
import pandas as pd
from button_bitid import Button
import csv
from collections import deque
import soco
import yeelight
from netifaces import interfaces, AF_INET, ifaddresses

# Used when embedded in autoid server
import sys
sys.path.append('../')


class detection:
    __xInput = {}
    __index = 0

    # 存放sensingEPC
    __sensingEPClist=[]
    # 存放interactionEPC
    __interactionEPClist=[]

    # 存放结果 
    __sensingResultdic = {}
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

    def detect_status(self, host, port,event,eventlist, dbHandler=None):
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
                    curRecord = {}
                    for item in datalist:
                        k = i % 9
                        if item == '':
                            continue
                        else:
                            if k == 1:
                                self.__xInput['EPC'].append(item)
                                self.epc_queue.append(item)
                                curRecord['EPC'] = item
                                curEPC = item
                            elif k == 2:
                                self.__xInput['Antenna'].append(int(item))
                                curRecord['Antenna'] = int(item) 
                            elif k == 3:
                                self.__xInput['Freq'].append(float(item))
                                curRecord['Freq'] = float(item)
                            elif k == 4:
                                ctime = float(item)
                                self.__xInput['ReaderTimestamp'].append(ctime)
                                curRecord['ReaderTimestamp'] = ctime 
                                self.readerTimestamp_queue.append(ctime)
                                # pop all items outside the sliding window
                                while len(self.readerTimestamp_queue) > 0:
                                    ptime = self.readerTimestamp_queue.popleft()
                                    if ctime - ptime > 200:
                                        self.epc_queue.popleft()
                                    else:
                                        self.readerTimestamp_queue.appendleft(ptime)
                                        break
                                for epc in self.__sensingEPClist:
                                    self.__sensingResultdic[epc] = bool(self.epc_queue.count(epc))
                                self.__lastresultlist = self.__interactionResultlist
                                self.__interactionResultlist = []
                                for epc in self.__interactionEPClist:
                                    self.__interactionResultlist.append(bool(self.epc_queue.count(epc)))
                                im = 0
                                # print(self.__interactionResultlist)
                                # self.__clickResultlist = []
                                for epc in self.__interactionEPClist:
                                    if self.__interactionResultlist[im]:
                                        if not self.__lastresultlist[im]:
                                            eventlist[im].set()
                                            print("true")
                                    #         self.__clickResultdic[epc] = "True"
                                    #     else:
                                    #         self.__clickResultdic[epc] = "False"
                                    # else:
                                    #     self.__clickResultdic[epc] = "False"
                                    im += 1

                            elif k == 5:
                                self.__xInput['RSSI'].append(float(item))
                                curRSSI = float(item)
                                curRecord['RSSI'] = curRSSI 
                            elif k == 6:
                                self.__xInput['Doppler'].append(float(item))
                                curRecord['Doppler'] = float(item) 
                            elif k == 7:
                                self.__xInput['Phase'].append(float(item))
                                curRecord['Phase'] = float(item)
                            elif k == 8:
                                ctStamp = timedelta(seconds=(float(item[:-1]) / 1000))
                                self.__xInput['ComputerTimestamp'].append(ctStamp)
                                curRecord['ComputerTimestamp'] = str(ctStamp) 
                            else:
                                self.updateEPC(curRSSI, curEPC)
                                if dbHandler is not None and curRecord != {}:
                                    dbHandler.saveRawData(curRecord)
                                    curRecord = {}
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
            return self.maxEPC 
        else:
            return 'None' 

    def updateSensingEPC(self,xEPClist):
        # print(xEPClist)
        self.__sensingEPClist = xEPClist

    def updateInteractionEPC(self,xEPClist):
        self.__interactionEPClist = xEPClist

    def getSensingresult(self):
        return self.__sensingResultdic

    def getInteractionresult(self):
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

    # bulb and sonos init
    sonos = list(soco.discover(timeout=10))[0]
    muteFlag = False
    bulb = yeelight.Bulb(yeelight.discover_bulbs(timeout=10)[0].get('ip'))

    # phone status
    phonestatus = False
    phoneEPC = 'E20000193907010113104906'

    sensingEPClist = ['E20000193907010113104906','E2000019390700191300052D','E2000019190B011910105997']
    r_event = threading.Event()
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
        t1.start()
        r_event.set()
        iiii = 0

        print(sonos)
        if sonos:
            sonos.play_mode = 'REPEAT_ONE'
            sonos.play_uri('http://img.tukuppt.com/newpreview_music/09/01/52/5c89f044e48f61497.mp3')
            sonos.volumn = 6
        print(bulb)
        if bulb:
            bulb.toggle()

        print("start!!!!")
        while True:
            # 获取phone的状态
            d.updateSensingEPC(sensingEPClist)
            sensingresult = d.getSensingresult()
            if sensingresult:
                if phoneEPC in sensingresult.keys():
                    if sensingresult[phoneEPC] == True:
                        phonestatus = True
                    else:
                        phonestatus = False
                else:
                    phonestatus = False
            else:
                phonestatus = False
            # press event
            d.updateInteractionEPC(EPClist)
            for event in eventlist:
                if event.is_set():
                    # 说明此时有点击事件
                    if phonestatus:
                        print("sonos.mute:",sonos.mute)
                        muteFlag = ~muteFlag
                        sonos.mute = muteFlag
                    else:
                        print("bulb lighted")
                        bulb.toggle()
                    print("true",iiii)
                    event.clear()
                    iiii += 1
    except KeyboardInterrupt as e:
        print ("Exiting...")
    finally:
        r_event.clear()
        t1.join()
