#!/usr/bin/python3
import pymongo as mongo
import datetime as datetime


class DataReader:
    def __init__(self):
        self.client = mongo.MongoClient("mongodb://101.6.114.5:27017")
        self.database = self.client["AutoID"]
        #self.database = self.client["test"]
        self.tagData = self.database["TagData"]
        self.timeFormat = "%Y-%m-%dT%H:%M:%S"
        self.timeDelta = 28800  # Beijing timezone is 8 hours faster than UTC

    def GetData(self, startTime, endTime, count=None):
        found = self.tagData.find({'Time': {'$lt': endTime, '$gte': startTime}})
        if count is None:
            return found
        else:
            return found[:count] if found.count() > count else found
    def PKTime(self, year, month, day, hour, minute, sec):
        return datetime.datetime(year, month, day, hour - 8, minute, sec)


if __name__ == '__main__':
    reader = DataReader()
    startTime = reader.PKTime(2018, 12, 12, 10, 40, 00)
    endTime = reader.PKTime(2018, 12, 12, 11, 40, 00)
    result = reader.GetData(startTime, endTime, 100)
    for item in result:
        print(item)
