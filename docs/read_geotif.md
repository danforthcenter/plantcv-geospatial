## Read Geo-tif Data

Read in data (from tif format, most likely georeferenced image data). 

**plantcv.geospatial.read_geotif**(*filename, bands="rgb"*)

**returns** [PlantCV Spectral_data](https://plantcv.readthedocs.io/en/latest/Spectral_data/) object instance 

- **Parameters:**
    - filename - Filepath to .tif data 
    - bands - Comma separated string representing the order of image bands (default bands="R,G,B"), or a list of wavelengths (e.g. bands=[650,560,480])
        - Supported keys for bands and their default_wavelengths = {"R": 650, "G": 560, "B": 480, "RE": 717, "N": 842, "NIR": 842}

- **Example use:**
    - below


```python
import plantcv.plantcv as pcv 
import plantcv.geospatial as geo

# Read geotif in
marker = geo.read_geotif(filename="./data/example_img.tif", bands="r,g,b,NIR,RE")

```

![Screenshot](documentation_images/multispec_pseudo_rgb.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/read_geotif.py)
