# Tectoniq
## Context
Something about lithium exploration.

## Getting Started
You require a Python installation to proceed. We recommend getting the latest stable version of Python. Setting up Python environments is also recommended if you are doing other work that relies on specific versions of libraries being installed.

If you have an NVIDIA GPU, consider installing the [CUDA toolkit](https://developer.nvidia.com/cuda-downloads).

Ensure you install the required packages by running:
```
python -m pip install -r packages.config
```

Also, separately install for plotting with no dependencies (requirements file do not support this flag):
```
python -m pip install basemap --no-deps
```

You also require the following for data imputation:
```
python -m pip install mxnet --no-deps
python -m pip install datawig
```

## Data
Some data files are included within the repository. Larger files must be obtained from the [Google Drive](https://drive.google.com/drive/folders/1tcuR22angp5zksqhrQ6BmQLoTms_ldLd).

## Projects
### Phase III
#### Part I (2023-08-22 - TBD)
* Ratio calcs reduced to only MnO_MgO - the rest were precalculated
* MnO_MgO column added
* < n PPM values substituted with n / 2
* Running histogram.ipynb produced:
*   - Confusions matrices for Li, Sb, Zn, Ag, Au, Sn at 200 and 1000ppm thresholds for Li and single thresholds for other elements
*   - Serialised HistogramGradientBoostingRegressor .joblib file trained & fitted on new geochem dataset

#### Part II (TBD)
* What files did we run
* What output did we produce and send?
* Anything to note...


#### Part III (TBD)

### Mercedes
...