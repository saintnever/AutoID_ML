import os
import numpy as np
import pandas as pd
import argparse
import sys
import csv
import arrow


input="./data/data_6trials_3people.csv"
outputfile="data_6trials_3people_beijing_ftime.csv"

out = open(outputfile,'a',newline='')
titlelist=['number','Ant','CRC','Count','EPC','Freq','PC','Phase','Protocol','RSSI','Time','id','timestamp']
csv_write = csv.writer(out,dialect='excel')
csv_write.writerow(titlelist)
    
with open(input) as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        time = row[10]
        utc = arrow.get(time)
        beijing = utc.naive.microsecond/1000000 + utc.naive.second + utc.naive.minute * 60 + utc.naive.hour * 60 * 60       
        row[10] = str(beijing)
        csv_write.writerow(row)
out.close()

