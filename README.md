# AutoID_ML
The deep learning codes for AutoID project

## Dependency
### MongoDB
The configure file on Windows server should set bindIP to 0.0.0.0 (listen to all IP) or specific network interface.
Use `pip3 install pymongo` to install in the python virtual environment.

## Usage
### DataReader
#### import as a module
``` python
reader = DataReader()
startTime = reader.PKTime(2018, 10, 10, 22, 30, 00) #2018/10/10 22:30 0s
endTime = reader.PKTime(2018, 12, 31, 23, 30, 30)
epc = "E200001939070049131014D4"
result = reader.GetData(startTime, endTime, 100, epc) # Tag with id epc's first 100 records in this interval
result = reader.GetData(startTime, endTime, 100) # 100 records from all tags in this interval
result = reader.GetData(startTime, endTime, None, epc) # Tag with id epc's all records in this interval
result = reader.GetData(startTime, endTime) # All records from all tags in this interval
```
#### Usage in terminal
`python3 DataReader.py -h` will give your help. Remember to launch correct virtual environment first.