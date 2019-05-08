from detection import detection
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
import copy
import yeelight
import pickle
from netifaces import interfaces, AF_INET, ifaddresses


if __name__ == '__main__':
    data = []
    # 开路和短路
    sensingEPClist = ['E2000019190B0086102035F3','E2000019190B00301030086F']
    # sensingEPClist = ['E2000019190B008910103834','E2000019190B0084102035F2']
    tag = [True,False]
    r_event = threading.Event()
    lasttime = 0
    slidetime = 0
    try:
        d = detection()
        eventlist = []
        t1 = threading.Thread(target=d.detect_status, args=('101.6.114.22',14,r_event,eventlist,))
        t1.start()
        r_event.set()
        last = 0
        statuslist = ["10","01"]
        laststatue_time = []
        slide_left = 0
        slide_right = 0
        while True:
            d.updateSensingEPC(sensingEPClist)
            sensingresult = d.getSensingresult()
            if sensingresult:
            # if list(sensingresult.values()).count(True) == 1:
                nowFalse = ""
                if sensingresult[sensingEPClist[0]] == tag[1]:
                    nowFalse += "1"
                else:
                    nowFalse += "0"
                if sensingresult[sensingEPClist[1]] == tag[1]:
                    nowFalse += "1"
                else:
                    nowFalse += "0"
                nowtime = time.time()
                if nowFalse == "01":
                    if laststatue_time:
                        if laststatue_time[0] == "10":
                            if nowtime-laststatue_time[1]<1:
                                slide_right += 1
                    laststatue_time = [nowFalse,nowtime]
                elif nowFalse == "10":
                    if laststatue_time:
                        if laststatue_time[0] == "01":
                            if nowtime-laststatue_time[1]<1:
                                slide_left += 1
                    laststatue_time = [nowFalse,nowtime]
                                  
    except KeyboardInterrupt as e:
        print("left",slide_left)
        print("right",slide_right)
        print ("Exiting...")
    finally:
        r_event.clear()
        t1.join()