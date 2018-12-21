import os
import numpy as np
import pandas as pd
import argparse
import sys
import csv


def compare(origin,output):
    # origin= "./data/data_neg.csv"
    # output="testnumber.csv"
    originlist=[]
    outputlist=[]
    with open(origin) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for rows in csv_reader:
            tmp = []
            for i in range(12):
                tmp.append(rows[i])
            originlist.append(tmp)
    with open(output) as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        for rows in csv_reader:
            tmp = []
            for i in range(12):
                tmp.append(rows[i])
            outputlist.append(tmp)
    i = len(outputlist)
    flag = True
    for tmp_i in range(i):
        for tmp_j in range(12):
            if(originlist[tmp_i][tmp_j] != outputlist[tmp_i][tmp_j]):
                if tmp_j != 7:
                    # global flag
                    flag = False
                    print("error!!!!!!!")
                    print(originlist[tmp_i][tmp_j])
    if flag:
        print("we are right!!!!!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="origindatafile",
                        help="origindatafile.For example, ./data/data_neg.csv ")
    parser.add_argument("--output", dest="outputdatafile", help="outputdatafile.")
    args = parser.parse_args()
    if args.inputfile:
        if args.outputfile:
            # global mi
            printf("start")
            # mi = 0
            compare(args.origindatafile,args.outputdatafile)
        else:
            print("please give the right args!")
    else:
        print("please give the right args!")