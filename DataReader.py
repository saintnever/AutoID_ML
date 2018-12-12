#!/usr/bin/python3
import pymongo as mongo
import datetime as datetime
import argparse
import re


class DataReader:
    def __init__(self):
        self.client = mongo.MongoClient("mongodb://101.6.114.5:27017")
        self.database = self.client["AutoID"]
        #self.database = self.client["test"]
        self.tagData = self.database["TagData"]
        self.timeFormat = "%Y-%m-%dT%H:%M:%S"
        self.timeDelta = 8  # Beijing timezone is 8 hours faster than UTC
    def GetData(self, startTime, endTime, count=None, epc=None):
        if epc is None:
            found = self.tagData.find({'Time': {'$lt': endTime, '$gte': startTime}})
        else:
            found = self.tagData.find({
                'Time': {'$lt': endTime, '$gte': startTime},
                'EPC': epc
            })
        if count is None:
            return found
        else:
            return found[:count] if found.count() > count else found
    def PKTime(self, year, month, day, hour, minute, sec):
        return datetime.datetime(year, month, day, hour - self.timeDelta, minute, sec)
    
if __name__ == '__main__':
    reader = DataReader()
    parser = argparse.ArgumentParser()
    parser.add_argument("--epc", dest = "epc", help = "The EPC of the tag you want to find. Ignore if you want all")
    parser.add_argument("--num", dest = "num", help = "How many data you want to get?")
    parser.add_argument("--start", dest = "start", help = "Start time. Format in  yyyy/MM/dd/HH/mm/ss", default = "2018/12/12/10/40/00")
    parser.add_argument("--end", dest = "end", help = "End time. Format in  yyyy/MM/dd/HH/mm/ss", default = "2018/12/12/11/40/00")
    args = parser.parse_args()
    startOpt = re.split('/', args.start) 
    startTime = reader.PKTime(int(startOpt[0]),int(startOpt[1]),int(startOpt[2]),int(startOpt[3]),int(startOpt[4]),int(startOpt[5]))
    endOpt = re.split('/', args.end) 
    endTime = reader.PKTime(int(endOpt[0]),int(endOpt[1]),int(endOpt[2]),int(endOpt[3]),int(endOpt[4]),int(endOpt[5]))
    result = reader.GetData(startTime, endTime, args.num, args.epc)
    for item in result:
        print(item)
