## Read Geo-tif Data

Read in data (from tif format, most likely georeferenced image data). 

**plantcv.geospatial.read_geotif**(*filename, mode="rgb"*)

**returns** [PlantCV Spectral_data](https://plantcv.readthedocs.io/en/latest/Spectral_data/) object instance 

- **Parameters:**
    - filename - Filepath to .tif data 
    - mode - Mode for geotif reading  

- **Context:**
    - Used to define a list of coordinates of interest.

- **Example use:**
    - below


```python
import plantcv.plantcv as pcv 
import plantcv.geospatial as geo

# Read geotif in
marker = geo.read_geotif(filename="./data/example_img.tif", mode="rgb")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/read_geotif.py)
