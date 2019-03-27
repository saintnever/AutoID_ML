from datetime import datetime, timedelta

class Button:
    EPC = ''
    buttonCount = 0

    def __init__(self,EPC):
        self.EPC = EPC
        Button.buttonCount += 1

    # 用来判断状态有没有发生变化，并且检测状态发生变化次数 
    def statusChange(self,df_data,wins,steps):
        clickedTime = 0
        lastclicked = False
        win = timedelta(seconds=wins)
        step = timedelta(seconds=steps)
        timeStart = df_data['ReaderTimestamp'].min()
        timeEnd = df_data['ReaderTimestamp'].max()
        time = timeStart
        while time < timeEnd:
            df_frame = df_data[(df_data['ReaderTimestamp'] >= time) & (df_data['ReaderTimestamp'] < time + win)]
            # 使用BitID的天线二数据
            ifexist = df_frame.loc[(df_frame['EPC']==self.EPC)]
            time += step
            # BCbutton
            # if not len(ifexist) == 0:
            #     # 防止产生按压很久的判断
            #     if not lastclicked:
            #         clickedTime += 1   
            #         lastclicked = True 
            # else:
            #     #考虑检测到的数量会不会产生误判
            #     lastclicked = False
            # SCbutton
            if len(ifexist) == 0:
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
    
    def rewinstatusChange(self,df_data):
        ifexist = df_data.loc[(df_data['EPC']==self.EPC)]
        if len(ifexist):
            return True
        else:
            return False

    def winstatusChangelist(self,xInput,start):
        for i in range(start,len(xInput['EPC'])):
            if xInput['EPC'][i] == self.EPC:
                return True
        return False
    
    def blockstatusChangelist(self,xInput,start,end):
        for i in range(start,end + 1):
            if xInput['EPC'][i] == self.EPC:
                return True
        return False

    def getspeed(self,df_data,wins,steps):
        timelist = []
        clickedTime = 0
        lastclicked = False
        win = timedelta(seconds=wins)
        step = timedelta(seconds=steps)
        timeStart = df_data['ReaderTimestamp'].min()
        timeEnd = df_data['ReaderTimestamp'].max()
        time = timeStart
        while time < timeEnd:
            df_frame = df_data[(df_data['ReaderTimestamp'] >= time) & (df_data['ReaderTimestamp'] < time + win)]
            # 使用BitID的天线二数据
            ifexist = df_frame.loc[(df_frame['EPC']==self.EPC)]
            time += step
            # BCbutton
            # if not len(ifexist) == 0:
            #     # 防止产生按压很久的判断
            #     if not lastclicked:
            #         clickedTime += 1   
            #         lastclicked = True 
            #         # print(ifexist[0:1]['ReaderTimestamp'])
            #         timelist.append(ifexist[0:1]['ReaderTimestamp'].values)
            # else:
            #     #考虑检测到的数量会不会产生误判
            #     lastclicked = False
            # SCbutton
            if len(ifexist) == 0:
                # 防止产生按压很久的判断
                if not lastclicked:
                    clickedTime += 1   
                    lastclicked = True 
                    # print(time)
                    timelist.append(time.total_seconds())
            else:
                #考虑检测到的数量会不会产生误判
                lastclicked = False
        return clickedTime,timelist