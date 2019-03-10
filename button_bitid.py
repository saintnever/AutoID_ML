from datetime import datetime, timedelta

class Button:
    EPC = ''
    buttonCount = 0

    def __init__(self,EPC):
        self.EPC = EPC
        Button.buttonCount += 1

    # 用来判断状态有没有发生变化，并且检测状态发生变化次数 
    def statusChange(self,df_data):
        clickedTime = 0
        lastclicked = False
        win = timedelta(seconds=1)
        step = timedelta(seconds=0.5)
        timeStart = df_data['ReaderTimestamp'].min()
        timeEnd = df_data['ReaderTimestamp'].max()
        time = timeStart
        while time < timeEnd:
            df_frame = df_data[(df_data['ReaderTimestamp'] >= time) & (df_data['Time'] < time + win)]
            # 使用BitID的天线二数据
            ifexist = df_frame.loc[(df_frame['EPC']==self.EPC) & (df_frame['Antenna']==2)]
            time += step
            # 0的话说明没有检测到
            if not len(ifexist) == 0:
                # 防止产生按压很久的判断
                if not lastclicked:
                    clickedTime += 1   
                    lastclicked = True 
            else:
                #考虑检测到的数量会不会产生误判
                lastclicked = False
        return clickedTime

    def winstatusChange(self,df_data):
        ifexist = df_data.loc[(df_data['EPC']==self.EPC) & (df_data['Antenna']==2)]
        if len(ifexist) >= 3:
            return True
        else:
            return False

    def winstatusChangelist(self,xInput,start):
        for i in range(start,len(xInput['EPC'])):
            if xInput['EPC'][i] == self.EPC:
                return True
        return False