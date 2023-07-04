#! /bin/bash

pydeps -o depgraph.svg --max-bacon 1 --reverse --include-missing -x numpy ipython sklearn pandas absl -- food_volume_estimation
pydeps -o depgraph_2.svg --max-bacon 2 --reverse  -x matplotlib.* numpy.* ipython.* sklearn.* pandas.* absl.* scipy.* IPython.* -- food_volume_estimation
pydeps -o depgraph_2_down.svg --max-bacon 2 -x matplotlib.* numpy.* ipython.* sklearn.* pandas.* absl.* scipy.* IPython.* -- food_volume_estimation
pydeps -o depgraph_4_down.svg --max-bacon 4 -x matplotlib.* numpy.* ipython.* sklearn.* pandas.* absl.* scipy.* IPython.* -- food_volume_estimation
pydeps -o depgraph_3.svg --max-bacon 3 --reverse  -x matplotlib.* numpy.* ipython.* sklearn.* pandas.* absl.* scipy.* IPython.* requests.* -- food_volume_estimation
pydeps -o depgraph_root.svg --max-bacon 2 --reverse  -x matplotlib.* numpy.* ipython.* sklearn.* pandas.* absl.* scipy.* IPython.* requests.* -- VolumeEstimation