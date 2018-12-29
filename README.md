# AutoID_ML
The deep learning codes for AutoID project

## branch description
6 trials of behavior sequences are performed by 3 participants. 

The sequence are  Swith on Lamp-Open drawer-Open drug bottle-Pick up Cups-Close drug bottle-Close drawer-Open laptop lid for 1 min- Pick up book from shelf and read for 1min-Close book and put it back on the shelf-Close laptop lid-Switch Off Lamp. 

6 BitIDs are deployed seperately on the lamp, drawer, drug bottle, cup, laptop lid, and book. 

Features: Using data from all 3 Antennas. Use data from 49 RFID tags. Use BitID tag for automatic lable. RSSI and PHASE averaged with win=2s and step =0.5s. No interpolation, fill nan with -100(RSSI)/0(Phase). (6trials_win2_step05_nointerpolation_multilabel.pkl)

CNN structure: 3x2Dconv + 1xFC  (learning_models.py)

Results: 98.6% training accuracy with training set size=27120. 99% test accuracy with test set size=679. 

