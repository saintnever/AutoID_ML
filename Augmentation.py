from DataReader import DataReader
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

if __name__ == '__main__':
    reader = DataReader()
    origRSSI = []
    origPhase = []
    controller = AugController()
    for line in reader.GetDataFromCSV('pos1_lopen.csv', 'desk'):
        if line['EPC'] == 'E20000193907005113101B4D':
            # print(line['RSSI'] + '/' + line['Phase'])
            origRSSI.append(line['RSSI'])
            origPhase.append(line['Phase'])
    # newRSSI = controller.Gaussian(origRSSI)
    newRSSI = controller.Shift(origRSSI, -1)
    newPhase = controller.Gaussian(origPhase)
    l = len(origRSSI)
    cnt = 0
    while cnt < l:
        print(str(origRSSI[cnt]) + '/' + str(newRSSI[cnt]))
        # print(str(origPhase[cnt]) + '/' + str(newPhase[cnt]))
        cnt = cnt + 1
    # print(newPhase)