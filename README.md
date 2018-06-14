# PrepNIfTI
PrepNIfTI is a collection of Python scripts for (pre)processing NIfTI images,
mainly for deep learning projects.

## Requirements
numpy, pandas, nibabel, h5py, argparse

The scripts has been tested on Ubuntu 16.04 with Python 3.5.2 and Python 2.7.12

## Function

apply_mask.py: apply ribbon masks on images

normalize_min_max.py: normalize image intensities to range [-1 1]

## Usage
```
python apply_mask --file --input input.mgz --mask mask.mgz --output output.mgz --side [entire,left,right]
python apply_mask --folder --input input/ --mask mask/ --output output/ --side [entire,left,right]
```

```
python normalize_min_max --file --input input.mgz --output input.mgz
python normalize_min_max --folder --input input/ --output input/
```

## Credit
Haomeng Zhang, Arizona State University (https://github.com/zhanghaomeng)

Liang Mi, Arizona State University

## Contact
Please contact icemiliang@gmail.com for any issues.
