# AutoID_ML
The deep learning codes for AutoID project

## fromback.py
```
# receivedata
t1 = threading.Thread(target=receivedata, args=())
# processdata
t2 = threading.Thread(target=processdata, args=())
# if you want to update epclist
updateEPC(newepclist)
# if you want to get the result
currentresult = getresult()
if currentresult:
    # the list is the result you need
```


