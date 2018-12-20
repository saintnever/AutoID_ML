import os
import numpy as np
import pandas as pd
import argparse
import sys
import csv

# to calculate the var
def phase_calibrate(inputfile,outputfile):
    file = inputfile
    # calibrate后的输出文件
    out = open(outputfile,'a',newline='')
    titlelist=['epc','frequency','phase']
    csv_write = csv.writer(out,dialect='excel')
    csv_write.writerow(titlelist)
    # 获取所有epc，查后去重
    epclist=[]
    with open(file) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for row in csv_reader:
            epclist.append(row[4])
    epc_set=set(epclist)
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
                    if row[1] == "1":
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
        minfre =  pd.Series(frelist).min()
        if frelist:
            print(frelist)
            phi_r = average_dic[str(minfre)]
            with open(file) as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)
                for row in csv_reader:
                    if row[4] == epc:
                        if row[1] == "1":
                            calibrated_phase = int(row[7])-average_dic[row[5]]+phi_r
                            if calibrated_phase < 0:
                                calibrated_phase += 180
                            varlist=[epc,row[5],calibrated_phase]
                            csv_write.writerow(varlist)
    out.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="inputfile",
                        help="inputfilename.For example, ./data/data_neg.csv ")
    parser.add_argument("--output", dest="outputfile", help="outputfilename.")
    args = parser.parse_args()
    if args.inputfile:
        if args.outputfile:
            phase_calibrate(args.inputfile,args.outputfile)
        else:
            print("please give the right args!")
    else:
        print("please give the right args!")
        