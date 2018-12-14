import numpy as np
import tensorflow as tf
from DataReader import DataReader
from datetime import datetime
import pandas as pd

reader = DataReader()

try:
    startTime = reader.PKTime(2018, 12, 12, 10, 40, 00)
    endTime = reader.PKTime(2018, 12, 12, 12, 40, 00)
    bitid = pd.read_csv('bitid_mapping.csv')
    result = reader.GetData_epc(startTime, endTime, epclist=list(bitid[bitid['location'] == 'desktop']['EPC']))
    print(result)

except KeyboardInterrupt as e:
    print(e)
