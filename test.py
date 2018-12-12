import numpy as np
import tensorflow as tf
from DataReader import DataReader

reader = DataReader()

try:
    startTime = "2018-12-10T17:30:00"
    endTime = "2018-12-10T18:30:00"
    result = reader.GetData(startTime, endTime, 100000)
    for item in result:
        print(item)

except KeyboardInterrupt as e:
    print(e)
