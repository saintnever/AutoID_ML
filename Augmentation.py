from DataReader import DataReader, LoadFromPickle
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class AugController:
    def __init__(self):
        pass
    def Gaussian(self, data, mv = 0, sig = 1):
        orig = np.array(data, 'int32')
        gs = np.random.normal(mv, sig, len(data)) 
        int_gs = np.array(gs, 'int32')
        new = orig + int_gs
        return new.tolist()
    def Shift(self, data, offset):
        orig = np.array(data, 'int32')
        shift = np.linspace(offset, offset, len(data))
        n_shift = np.array(shift, 'int32')
        new = orig + n_shift
        return new.tolist() 
    def PreprocessData(self, fileName, objName, timeStep = 0.5):
        reader = DataReader()
        for line in reader.GetDataFromCSV(fileName, objName):
            pass
            

if __name__ == '__main__':
    reader = DataReader()
    x, y = LoadFromPickle()
    print(x)
    print('------------------')
    print(y)
    # origRSSI = []
    # origRSSI1 = []
    # origPhase = []
    # controller = AugController()
    # for line in reader.GetDataFromCSV('pos1_close.csv', 'desk'):
    #     # if line['EPC'] == 'E200001939070030131007FF':
    #     origRSSI.append(line['RSSI'])
    #     origPhase.append(line['Phase'])
    # for line in reader.GetDataFromCSV('pos2_close.csv', 'desk'):
    #     # if line['EPC'] == 'E2000019390700821310357D':
    #     origRSSI1.append(line['RSSI'])
    # newRSSI = controller.Gaussian(origRSSI)
    # # newRSSI = controller.Shift(origRSSI, -1)
    # newPhase = controller.Gaussian(origPhase)
    # l = len(origRSSI)
    # cnt = 0
    # while cnt < l:
    #     print(int(origRSSI[cnt])/int(newRSSI[cnt]))
    #     cnt = cnt + 1
    # # print(newPhase)