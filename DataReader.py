#!/usr/bin/python3
import pymongo as mongo
import datetime as datetime
import argparse
import re
import json

configFile = "TagInfo.json"


class DataReader:
    def __init__(self):
        self.client = mongo.MongoClient("mongodb://101.6.114.5:27017")
        # self.database = self.client["AutoID"]
        self.database = self.client["test"]
        self.tagData = self.database["TagData"]
        self.timeFormat = "%Y-%m-%dT%H:%M:%S"
        self.timeDelta = 8  # Beijing timezone is 8 hours faster than UTC
        with open(configFile, "r") as f:
            self.tagMap = json.load(f)
        self.allTag = []
        for key in self.tagMap.keys():
            tagList = self.tagMap[key]
            for tag in tagList:
                self.allTag.append(tag)

    def GetData(self, startTime, endTime, count=None, objName=None):
        if objName is None:
            epcList = self.allTag
        else:
            if objName not in self.tagMap.keys():
                print("Invalid object name. Please see README or TagInfo.json")
                return []
            else:
                epcList = self.tagMap[objName]
        print(epcList)
        result = self.GetData_epc(startTime, endTime, count, epcList) 
        return result
        # if epcList is None:
        #     epcList = self.allTag
        # for epc in epcList:
        #     if epc is None:
        #         found = self.tagData.find({'Time': {'$lt': endTime, '$gte': startTime}})
        #     else:
        #         found = self.tagData.find({
        #             'Time': {'$lt': endTime, '$gte': startTime},
        #             'EPC': epc
        #         })
        #     for item in found:
        #         result.append(item)
        # if count is None:
        #     return result
        # else:
        #     return result[:count] if len(result) > count else result

    def GetData_epc(self, startTime, endTime, count=None, epclist=None):
        if epclist is None:
            found = self.tagData.find({'Time': {'$lt': endTime, '$gte': startTime}})
        else:
            found = self.tagData.find({
                'Time': {'$lt': endTime, '$gte': startTime},
                'EPC': {'$in': epclist}
            })
        # convert the cursor into a list
        results = list(found)
        if count is None:
            return results
        else:
            return results[:int(count)] if len(results) > int(count) else results

    def PKTime(self, year, month, day, hour, minute, sec):
        return datetime.datetime(year, month, day, hour - self.timeDelta, minute, sec)


if __name__ == '__main__':
    reader = DataReader()
    parser = argparse.ArgumentParser()
    parser.add_argument("--obj", dest="obj",
                        help="The object you want to find, automatically mapping to epc colleciton. Ignore if you want all")
    parser.add_argument("--num", dest="num", help="How many data you want to get?")
    parser.add_argument("--start", dest="start", help="Start time. Format in  yyyy/MM/dd/HH/mm/ss",
                        default="2018/12/12/10/40/00")
    parser.add_argument("--end", dest="end", help="End time. Format in  yyyy/MM/dd/HH/mm/ss",
                        default="2018/12/12/11/40/00")
    args = parser.parse_args()
    startOpt = re.split('/', args.start)
    startTime = reader.PKTime(int(startOpt[0]), int(startOpt[1]), int(startOpt[2]), int(startOpt[3]), int(startOpt[4]),
                              int(startOpt[5]))
    endOpt = re.split('/', args.end)
    endTime = reader.PKTime(int(endOpt[0]), int(endOpt[1]), int(endOpt[2]), int(endOpt[3]), int(endOpt[4]),
                            int(endOpt[5]))
    result = reader.GetData(startTime, endTime, args.num, args.obj)
    if result is not None:
        for item in result:
            print(item)
