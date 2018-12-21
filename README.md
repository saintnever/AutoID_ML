# AutoID_ML
The deep learning codes for AutoID project

## branch description
A drawer is placed on a desk. The goal is to detect 1. the position of the drawer 2. the status of the drawer 

States : 2 positions with 3 drawer status (close/small open/large open) = 6 states  

Features: Only using data from ceiling Antenna (ANT2). Only using the data from the tags on the drawer. RSSI and PHASE averaged with win=2s and step =0.5s. 

Results: 99.3% training accuracy with training set size=84128. 100% test accuracy with training set size=2630. 

