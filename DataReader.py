#!/usr/bin/python3
import pymongo as mongo
from datetime import datetime

class DataReader:
    def __init__(self):
        self.client = mongo.MongoClient("mongodb://101.6.114.5:27017")
        self.database = self.client["AutoID"] 
        self.tagData = self.database["TagData"]
    def GetData(self, date, startTime, endTime, count = 100):
        myQuery = {"Time": {"$regex": "^" + date}}
        found = self.tagData.find(myQuery);
        result = []
        cnt = 0
        for item in found:
            time = int(item["Time"][11:13])
            if(time <= endTime and time >= startTime):
                result.append(item)
                cnt = cnt + 1
            if(cnt > count):
                break
        return result


if __name__ == '__main__':
    reader = DataReader()
    result = reader.GetData("2018-12-06", 17, 17, 50)
    for item in result:
        print(item)
