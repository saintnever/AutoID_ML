# AutoID_ML
The deep learning codes for AutoID project

## branch description
draw the heatmap using the 6_trial_sequence data

###smoothing.py 
Using data from Ant 1. Use data from tags on the table.  RSSI is averaged with win=2s and step =0.5s. No interpolation, fill nan with -100(RSSI)/0(Phase). 
The processed data of each tag is stored in a pickle file.

###raise.py
Using the smooth function to get data.

###plotheat.py
Draw heat map.
@Parameter: starttime endtime
@Output: a heatmap

###drawheatmap_sample
a sample using function drawheatmap to draw a heatmap

