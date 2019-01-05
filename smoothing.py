import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import pickle
import csv

def smooth(epc):
    # epc = "E2000019390701391310743D"
    file = "data_6trials_3people_beijing_ftime.csv"
    mylist=[]
    with open(file) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for row in csv_reader:
            if row[1] == "1":
                if row[4] == epc:
                    data = []
                    data= [int(row[9]),float(row[10])]
                    # print(data)
                    mylist.append(data)
    WIN = 2
    STEP = 0.5
    resultlist=[] #存储结果
    half_second_list=[] #0.5秒为一个标志
    start = mylist[0][1] #起始时间

    steptime = 32210
    tmp=[]

    # 先0.5秒滑动 把0.5秒的归在一个list里面
    for number in mylist:
        # print(str(number[1])+","+str(steptime))
        if number[1] - steptime <= STEP:
            tmp.append(number[0])
        else:
            while number[1] - steptime > STEP:
                half_second_list.append(tmp)
                tmp=[]
                steptime += STEP
            if number[1] - steptime <= STEP:
                tmp.append(number[0])
    half_second_list.append(tmp)

    steptime = 32210

    # 再把2秒作为一个窗口，求平均值
    steptime = 32210
    length = len(half_second_list)
    # print(length)

    for i in range(length):
        bigwin = half_second_list[i]
        if i < length - 3:
            bigwin += half_second_list[i+1] + half_second_list[i+2] + half_second_list[i+3]
        elif i == length - 3:
            bigwin += half_second_list[i+1] + half_second_list[i+2]
        elif i == length - 2:
            bigwin += half_second_list[i+1]
        # print(bigwin)
        if len(bigwin) == 0:
            tmp = [steptime,-100]
            resultlist.append(tmp)
        else:
            mean = np.mean(bigwin)
            # print(mean)
            tmp = [steptime,mean]
            resultlist.append(tmp)
        steptime += 0.5

    picklefilename = epc+'.pkl'
    output = open(picklefilename, 'wb')
    pickle.dump(resultlist, output)
    output.close()
    
        
