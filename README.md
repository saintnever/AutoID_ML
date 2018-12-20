# AutoID_ML
The deep learning codes for AutoID project

## Usage
### Calibration
#### import function phase_calibrate
``` python
from calibration import phase_calibrate

input="./data/data_neg.csv"
output="allepcneg.csv"
phase_calibrate(input,output)
```
#### Usage in terminal
`python3 calibration.py -h` will give your help like below:
``` bash
-h, --help           show this help message and exit
  --input INPUTFILE    inputfilename.For example, ./data/data_neg.csv
  --output OUTPUTFILE  outputfilename.
```