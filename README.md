# PrepNIfTI
PrepNIfTI is a collection of Python scripts for (pre)processing NIfTI images,
mainly for deep learning projects.

## Requirements
numpy, pandas, nibabel, h5py, argparse

The program has been tested on Ubuntu 16.04 with Python 3.5.2 and Python 2.7.12

## Function

apply_mask.py: apply ribbon masks on images

## Usage
```
python apply_mask --file --input input.mgz --mask mask.mgz --output input.mgz --side [entire,left,right]
```

## Credit
Haomeng Zhang, Arizona State University (https://github.com/zhhmzhang)

Liang Mi, Arizona State University

## Contact
Please contact icemiliang@gmail.com for any issues.
