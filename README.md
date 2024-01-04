# Introduction
SeisWiz is a collection of handy seismic loading, processing, and visualization functions for seismic data. It has
been designed specifically keeping in mind the needs of machine learning-based seismic interpretation projects in Python.
However, certain functions may also find their uses for non-interpretation applications. Some of the functions that are
currently supported (or we intend to support in the future) include:

1. Loading unstructured seismic volumes in Python from .segy files
2. Performing common processing operations to loaded volumes, including scaling, nomalization etc.
3. Visualizing seismic data in both 3D and 2D, co-rendering ML predictions with the original seismic etc. 
4. Reading ML predictions or processed seismic volumes back into formats compatible with professional interpretaion
   softwares such as Petrel, OpendTect etc.

  