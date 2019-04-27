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
    
    # sensingEPClist = ['E2000019190B009110104045','E2000019190B009310104046','E2000019190B003610300D6A']
    sensingEPClist = ['E2000019190B009510104047','E2000019190B009710104048','E2000019190B01001010460A']
    tag = [True,False]
    r_event = threading.Event()
    # 保证在中间位置才可以触发
    flag = False
    slidetime = 0
    try:
        d = detection()
        eventlist = []
        data=[]
        t1 = threading.Thread(target=d.detect_status, args=('101.6.114.22',14,r_event,eventlist,))
        t1.start()
        r_event.set()
        lastFalse = []
        last = 0
        statuslist = ["100","010","001"]
        starttime = 0
        window = []
        while True:
            # 获取三个EPC的状态
            d.updateSensingEPC(sensingEPClist)
            sensingresult = d.getSensingresult()
            if sensingresult:
            # if list(sensingresult.values()).count(True) == 1:
                nowFalse = ""
                if sensingresult[sensingEPClist[0]] == tag[0]:
                    nowFalse += "1"
                else:
                    nowFalse += "0"
                if sensingresult[sensingEPClist[1]] == tag[0]:
                    nowFalse += "1"
                else:
                    nowFalse += "0"
                if sensingresult[sensingEPClist[2]] == tag[0]:
                    nowFalse += "1"
                else:
                    nowFalse += "0"

                # print(nowFalse)
                # print(nowFalse)
                nowtime = time.time()
                if nowFalse in statuslist:
                    data.append([nowFalse,nowtime])
                if starttime == 0:
                    starttime = nowtime
                if nowtime  - starttime >= 0.5:
                    window_cal = []
                    for item in window:
                        if item in statuslist:
                            window_cal.append(statuslist.index(item))
                    # print(window_cal)
                    amount_0 = 0
                    count_0 = 1
                    amount_1 = 0
                    count_1 = 1
                    amount_2 = 0
                    count_2 = 1
                    for i in range(len(window_cal)):
                        if window_cal[i] == 0:
                            amount_0+= i
                            count_0 += 1
                        elif window_cal[i] == 1:
                            amount_1+= i
                            count_1 += 1
                        elif window_cal[i] == 2:
                            amount_2 += i
                            count_2 += 1
                    print(amount_0/count_0,amount_1/count_1,amount_2/count_2)
                    cal_0 = amount_0/count_0
                    cal_1 = amount_1/count_1
                    cal_2 = amount_2/count_2
                    countlist = [cal_0,cal_1,cal_2]
                    if countlist.count(0) == 2:
                        if not cal_1 == 0:
                            flag = True
                    if countlist.count(0) == 1:
                        if flag:
                            if cal_0 == 0:
                                if cal_1 < cal_2:
                                    print("right")
                                    slidetime+=1
                                # else:
                                    # print("left")
                                    # slidetime+=1
                                flag = False
                            # elif cal_1 == 0:
                            #     if cal_0 < cal_2:
                            #         print("right")
                            #     else:
                            #         print("left")
                            #         slidetime+=1
                            #     flag = False
                            elif cal_2 == 0:
                                if cal_0 > cal_1:
                                    print("left")
                                # else:
                                #     print("left")
                                    # slidetime+=1
                                flag = False
                    # elif countlist.count(0) == 0:
                    #     if cal_0 < cal_2:
                    #         print("left")
                    #     if cal_0 > cal_2:
                    #         print("right")

                    # print(amount)
                    starttime = nowtime
                    # print(window)
                    window = window[int(len(window)/4*3):]
                    # window = []
                else:
                    window.append(nowFalse)

            # # ~~~~~~~~~~~~~~~~~~~~~~~
            # if sensingresult:
            #     # print(sensingresult)
            #     if list(sensingresult.values()).count(False) == 1:
            #         # print(sensingresult)
            #         nowFalse = ""
            #         if sensingresult['E2000019190B009510104047'] == False:
            #             nowFalse += "1"
            #         else:
            #             nowFalse += "0"
            #         if sensingresult['E2000019190B009710104048'] == False:
            #             nowFalse += "1"
            #         else:
            #             nowFalse += "0"
            #         if sensingresult['E2000019190B01001010460A'] == False:
            #             nowFalse += "1"
            #         else:
            #             nowFalse += "0"
            #         # print(nowFalse)
            #         # print(nowFalse,lastFalse)
            #         if nowFalse == "010":
            #             # print(nowFalse,lastFalse)
            #             # exit(10)
            #             # print(lastFalse)
            #             # exit(10)
            #             if lastFalse.count("100") > lastFalse.count("001"):
            #                 print("right")
            #             elif lastFalse.count("100") < lastFalse.count("001"):
            #                 print("left")
            #         elif lastFalse:
            #             if lastFalse[len(lastFalse)-1] =="010":
            #                 if nowFalse == "100":
            #                     print("left")
            #                 elif nowFalse == "001":
            #                     print("right")
            #         if len(lastFalse) > 5:
            #             lastFalse.remove(lastFalse[0])
            #             lastFalse.append(nowFalse)
            #         else:
            #             lastFalse.append(nowFalse)
            #         # print(nowFalse,lastFalse)
            # # ~~~~~~~~~~~~~~~~~~
                        # ~~~~~~~~~~~~~~~~~~~~~~~
            # if sensingresult:
            #     # print(sensingresult)
            #     if list(sensingresult.values()).count(True) == 1:
            #         # print(sensingresult)
            #         nowFalse = ""
            #         if sensingresult['E2000019190B0046103012F7'] == True:
            #             nowFalse += "1"
            #         else:
            #             nowFalse += "0"
            #         if sensingresult['E2000019190B01041010460C'] == True:
            #             nowFalse += "1"
            #         else:
            #             nowFalse += "0"
            #         if sensingresult['E2000019190B0044103012F6'] == True:
            #             nowFalse += "1"
            #         else:
            #             nowFalse += "0"
            #         # print(nowFalse)
            #         # print(nowFalse,lastFalse)
            #         if nowFalse == "010":
            #             # print(nowFalse,lastFalse)
            #             # exit(10)
            #             # print(lastFalse)
            #             # exit(10)
            #             if lastFalse.count("100") > 1 and lastFalse.count("100") > lastFalse.count("001"):
            #                 print("right")
            #             elif lastFalse.count("001") >1 and lastFalse.count("100") < lastFalse.count("001"):
            #                 print("left")
            #         # elif lastFalse:
            #         #     if lastFalse[len(lastFalse)-1] =="010":
            #         #         if nowFalse == "100":
            #         #             print("left")
            #         #         elif nowFalse == "001":
            #         #             print("right")
            #         if len(lastFalse) > 5:
            #             lastFalse.remove(lastFalse[0])
            #             lastFalse.append(nowFalse)
            #         else:
            #             lastFalse.append(nowFalse)
            #         # print(nowFalse,lastFalse)
            # # ~~~~~~~~~~~~~~~~~~
            # #         if nowFalse in statuslist:
            # #             tmp = statuslist.index(nowFalse)
            # #             # print(nowFalse)
            # #             if tmp > last:
            # #                 print(nowFalse)
            # #                 print("right")
            # #                 last = tmp
            # #             if tmp < last:
            # #                 print(nowFalse)
            # #                 print("left")
            # #                 last = tmp
            #             # print(i,lastFlase)
            # # 使用中间标签作为标定，然后其他标签作为非标定
            # # if sensingresult:
            # #     if list(sensingresult.values()).count(True) == 1:
            # #         nowFalse = ""
            # #         if sensingresult['E2000019190B0046103012F7'] == True:
            # #             nowFalse += "1"
            # #         else:
            # #             nowFalse += "0"
            # #         if sensingresult['E2000019190B01041010460C'] == True:
            # #             nowFalse += "1"
            # #         else:
            # #             nowFalse += "0"
            # #         if sensingresult['E2000019190B0044103012F6'] == True:
            # #             nowFalse += "1"
            # #         else:
            # #             nowFalse += "0"
                    
            # #         # if nowFalse == "010":
            # #         #     if lastFalse == "100":
            # #         #         print("right")
            # #         #     elif lastFalse == "001":
            # #         #         print("left")
            # #         # elif lastFalse == "010":
            # #         #     if nowFalse =="100":
            # #         #         lastFalse =  ""
            # #         #         print("left")
            # #         #     elif nowFalse == "001":
            # #         #         lastFalse = ""
            # #         #         print("right")
            # #         # lastFalse = nowFalse
            # #         # print(nowFalse,lastFalse)
            # #             if nowFalse in statuslist:
            # #                 tmp = statuslist.index(nowFalse)
            # #                     # # print(nowFalse)
            # #                 if tmp == 1 and last == 0:
            # #                     print("right")
            # #                 if tmp == 1 and last == 2:
            # #                     print("left")
            # #                 if tmp == 0 and last == 1:
            # #                     print("left")
            # #                 # IF tmp == 
            # #                 # if tmp < 1:
            # #                 #     print("left")
            # #                 last = tmp
                    
                    
    except KeyboardInterrupt as e:
        print(slidetime)
        with open('./data_slide/3dprint_open_right_20mm_s.pickle', 'wb') as f:
            pickle.dump(data, f)
        print ("Exiting...")
    finally:
        r_event.clear()
        t1.join()