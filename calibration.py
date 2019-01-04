import os
import numpy as np
import pandas as pd
import argparse
import sys
import csv
import matplotlib.pyplot as plt

def fit(x,y):
    if len(x) != len(y):
        return
    numerator = 0.0
    denominator = 0.0
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    for i in range(len(x)):
        numerator += (x[i]-x_mean)*(y[i]-y_mean)
        denominator += np.square((x[i]-x_mean))
    print('numerator:',numerator,'denominator:',denominator)
    b0 = numerator/denominator
    b1 = y_mean - b0*x_mean
    return b0,b1


# 定义预测函数
def predit(x,b0,b1):
    return b0*x + b1

# to calculate the var
def phase_calibrate(inputfile,outputfile):
    bolist=[]
    file = inputfile
    # calibrate后的输出文件
    out = open(outputfile,'a',newline='')
    titlelist=['number','Ant','CRC','Count','EPC','Freq','PC','Phase','Protocol','RSSI','Time','id']
    csv_write = csv.writer(out,dialect='excel')
    csv_write.writerow(titlelist)
    Antlist=["1"]
    # 获取所有epc，查后去重
    epclist=[]
    with open(file) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for row in csv_reader:
            epclist.append(row[4])
    epc_set=set(epclist)
    print("shdjkashdkjashdakjsdhakjsdhaksjdhaksjdhakjsdhakj")
    print(len(epc_set))
    for ant in Antlist:
        for epc in epc_set:
            frequency_dic = {}
            number_dic={}
            frelist=[]
            var_dic={}
            print(epc)
            with open(file) as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)
                for row in csv_reader:
                    if row[4] == epc:
                        if row[1] == ant:
                            if row[5] in frequency_dic:
                                var_dic[row[5]].append(int(row[7]))
                                frequency_dic[row[5]] += int(row[7])
                                number_dic[row[5]] += 1
                            else:
                                varlist=[]
                                varlist.append(int(row[7]))
                                var_dic[row[5]]=varlist
                                frelist.append(int(row[5]))
                                frequency_dic[row[5]] = int(row[7])
                                number_dic[row[5]] = 1
            average_dic = {}
            for key in frequency_dic:
                vartmp=pd.Series(var_dic[key]).std()
                # 解决跨越180的问题
                if vartmp > 50:
                    meantmp = pd.Series(var_dic[key]).mean()
                    for every in var_dic[key]:
                        if every < meantmp:
                            frequency_dic[key] += 180
                average_dic[key] = frequency_dic[key] / number_dic[key]
            if frelist: 
                #求基准频率
                frequency_array=[]
                average_array=[]
                for key in frequency_dic:
                    frequency_array.append(int(key))
                frequency_array.sort()
                for key in frequency_array:
                    average_array.append(average_dic[str(key)])
                length = len(average_array)
                # 如果只有一个频率，那么无法通过线性回归求取基准频率，为了防止产生nan，直接取原值，需要注意
                if length == 1:
                    fr = average_array[0]
                else :
                    base = 0
                    average_array_after=[]
                    average_array_after.append(average_array[0])
                    for tmp_i in range(1,length):
                        if average_array[tmp_i] - average_array[tmp_i-1] > 0:
                            base += 180
                            average_array_after.append(average_array[tmp_i]-base)
                        else:
                            average_array_after.append(average_array[tmp_i]-base)
                    b0,b1=fit(frequency_array,average_array_after)
                    bolist.append(b0)
                    print("b0 is " + str(b0))
                    if 902750 in frequency_array:
                        fr = average_array[0]
                        print("we have 902750!")
                    else:
                        # base = 0
                        # average_array_after=[]
                        # average_array_after.append(average_array[0])
                        # for tmp_i in range(1,length):
                        #     if average_array[tmp_i] - average_array[tmp_i-1] > 0:
                        #         base += 180
                        #         average_array_after.append(average_array[tmp_i]-base)
                        #     else:
                        #         average_array_after.append(average_array[tmp_i]-base)
                        # b0,b1=fit(frequency_array,average_array_after)
                        # print("b0 is " + str(b0))
                        fr = predit(902750,b0,b1)
                        while fr > 180:
                            fr -= 180
                print(frequency_array)
                # phi_r = average_dic[str(minfre)]
                phi_r = fr
                with open(file) as csvfile:
                    csv_reader = csv.reader(csvfile)
                    headers = next(csv_reader)
                    for row in csv_reader:
                        if row[1] == ant:
                            if row[4] == epc:
                                calibrated_phase = int(row[7])-average_dic[row[5]]+phi_r
                                if calibrated_phase < 0:
                                    calibrated_phase += 180
                                    # ['number','Ant','CRC','Count','EPC','Freq','PC','Phase','Protocol','RSSI','Time','id']
                                varlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],calibrated_phase,row[8],row[9],row[10],row[11]]
                                csv_write.writerow(varlist)
    out.close()
    plt.scatter(range(0,len(bolist)), bolist, s=50)
    plt.show()
    plt.savefig("b0.png")
# mi = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="inputfile",
                        help="inputfilename.For example, ./data/data_neg.csv ")
    parser.add_argument("--output", dest="outputfile", help="outputfilename.")
    args = parser.parse_args()
    if args.inputfile:
        if args.outputfile:
            # global mi
            printf("start")
            # mi = 0
            phase_calibrate(args.inputfile,args.outputfile)
        else:
            print("please give the right args!")
    else:
        print("please give the right args!")
        
