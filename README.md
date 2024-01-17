# 💡 Introduction
SeisWiz is a collection of handy seismic loading, processing, and visualization functions for seismic data. It has
been designed specifically keeping in mind the needs of machine learning-based seismic interpretation projects in Python.
However, certain functions may also find their uses for non-interpretation applications. Some of the functions that are
currently supported (or we intend to support in the future) include:

1. Loading unstructured seismic volumes in Python from .segy files
2. Performing common processing operations to loaded volumes, including scaling, nomalization etc.
3. Visualizing seismic data in both 3D and 2D, co-rendering ML predictions with the original seismic etc. 
4. Reading ML predictions or processed seismic volumes back into formats compatible with professional interpretaion
   softwares such as Petrel, OpendTect etc.

# 💻 Installation
To install SeisWiz, first create an Anaconda environment in a terminal by running
```commandline
conda create --name seismic_viewer python=3.7
```

Next clone the repository by running
```commandline
git clone https://github.com/amustafa9/SeisWiz.git
```

Afterwards, install the required packages by running 
```commandline
cd SeisWiz
pip install -r requirements.txt
```

# 🏃 Running SeisWiz
The current version of Seiswiz can be used in three basic modes:
1. Viewing a seismic volume by itself
2. Loading a specific horizon file along with the seismic volume of interest 
3. Bulk loading multiple horizon files along with a specific seismic volume

## Loading a Seismic Volume on SeisWiz
To visualize a specific seismic volume contained in a `.segy` file, run
```commandline
python scripts/main.py -i <path/to/segy>
```
This should bring up a matplotlib figure like the one shown below:
![image](figs/basic_mode_grayscale.gif)

[write instructions explaining the figure above]  

To render the seismic data in a different colormap, you can specify a matplotlib-compatible 
colormap using the `-cmap` argument. See example below:

```commandline
python scripts/main.py -i <path/to/segy> -cmap PRGn
```

This should render the volume in the specified colormap, as below: 
![image](figs/basic_mode_color.png)

## Loading a Seismic Volume on SeisWiz along with a Specific Horizon File
Seiswiz requires horizon picks to be contained in a text file in three columns in this order: inline, crossline, time/depth. 
The columns are separated by spaces and should have no names or other header information. An example of a horizon file
formatted in this manner is shown in the screenshot below: 

![image](figs/horizon_file_formatting.png)

Running Seiswiz to visualize a seismic volume with the horizon of interest superimposed is done by 
running

```commandline
python scripts/main.py -i <path/to/segy> -hor <path/to/horizon>
```

Executing this should result in the following interactive window popping up: 

![image](figs/one_horizon.gif)

## Loading a Seismic Volume on SeisWiz along with a Multiple Horizon Files
To simultaneously load multiple horizon files, place them all in a folder and pass the path to this 
folder as shown in the command below:

```commandline
python scripts/main.py -i <path/to/segy> -hor <path/to/horizon/folder>
```

This should result in the following interactive plot where multiple horizons can be 
visualized along with the seismic in the background. 

![image](figs/all_horizons.gif)

# 🔧 Issues 
If you run into any issues with installation or execution of the instructions above, please feel free to reach out to me 
at <span style="color:red"> ahmadmustafa.am@gmail.com </span>. Alternatively, you may create an issue on GitHub and I will look into it.

