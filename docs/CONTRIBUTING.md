# Contrbution to PlantCV-Geospatial

!!! note 
    PlantCV-Geospatial is an add-on package to PlantCV so please first refer to the main package's [contributing guide](https://plantcv.readthedocs.io/en/latest/CONTRIBUTING/) for the majority of the information on what and how to contribute to either project (including but not limited to reporting bugs, requesting new features, add/revise documentation, and adding tutorials). 

## Overview Of What To Contribute to PlantCV-Geospatial vs. Other Packages 

This document aims to give an overview of what to contribute to PlantCV-Geospatial, and guidelines to
decide which repository is the most appropriate place for new features. Please 
[create an issue in GitHub](https://github.com/danforthcenter/plantcv-geospatial/issues) assuming one
does not already exist.

Functions in the Geospatial toolbox are specific to UAV, satellite, and other types of 
georeferenced data. 

## PlantCV-Geospatial Tutorials

Many geospatial workflows require the use of the InteractiveShapes viewer object, which opens a Napari window outside of the jupyter notebook. These functions cannot currently be tested using our Github actions method, but it is useful to test as many steps in tutorials as we can. If you would like to contribute a geospatial tutorial that requires a Napari window, please follow these steps:

1. Once your notebook (`index.ipynb`) is finished, create a copy of that notebook and name it `test-index.ipynb`. 
2. Work through `test-index.ipynb` and comment out any steps requiring Napari.
3. Because the InteractiveShapes viewer object is often used to create shapefiles for downstream steps, generate those shapefiles and add them to a folder in the tutorial directory called `./shapefiles/`. 
4. Update the steps in `test-index.ipynb` requiring shapefiles to include the `./shapefiles/` directory in the file path. 
    -  Example: `gcv.analyze.color(img=ortho1, bin_mask=plant_mask, geojson="./experimental_plots.geojson")` becomes `gcv.analyze.color(img=ortho1, bin_mask=plant_mask,geojson="./shapefiles/experimental_plots.geojson")`. 
    - **Note**: it is a good idea to change the file paths in the original `index.ipynb` too so that users will know they can find a pre-generated version of necessary shapefiles in the tutorial folder. 
5. Modify the file in the tutorial repository `./tests/tests.py` on line number 10 to open `test-index.ipynb` instead of `index.ipynb`. Line 10 should read: `with open("test-index.ipynb", "r") as f:`

Now your tutorial can be automatically tested! Don't forget that if you make substantial changes to the tutorial notebook, you will have to change the test notebook to reflect those changes as well. 
