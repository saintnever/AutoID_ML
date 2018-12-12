#!/usr/bin/python3
import pymongo as mongo
import time


class DataReader:
    def __init__(self):
        self.client = mongo.MongoClient("mongodb://101.6.114.5:27017")
        self.database = self.client["AutoID"]
        self.tagData = self.database["TagData"]
        self.timeFormat = "%Y-%m-%dT%H:%M:%S"
        self.timeDelta = 28800  # Beijing timezone is 8 hours faster than UTC

    def GetData(self, startTime, endTime, count=100):
        start = int(time.mktime(time.strptime(startTime, self.timeFormat))) - self.timeDelta
        end = int(time.mktime(time.strptime(endTime, self.timeFormat))) - self.timeDelta
        found = self.tagData.find()
        result = []
        cnt = 0
        for item in found:
            timeStr = item["Time"][0:19]
            timeStamp = int(time.mktime(time.strptime(timeStr, self.timeFormat)))
            if (timeStamp >= start and timeStamp <= end):
                # Suppose the time is strictly increasing
                result.append(item)
                cnt = cnt + 1
            elif (timeStamp > end):
                break

            if (cnt >= count):
                break
        return result


if __name__ == '__main__':
    reader = DataReader()
    startTime = "2018-12-05T13:00:00"
    endTime = "2018-12-08T17:00:00"
    result = reader.GetData(startTime, endTime, 100000)
    for item in result:
        print(item)
