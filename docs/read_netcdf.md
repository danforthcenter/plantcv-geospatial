## Read NASA-formatted NetCDF Data

Read in data from a NetCDF file, formatted as NASA data downloads with all bands contained in the geophysical data group variables. 

**plantcv.geospatial.read.netcdf**(*filename, cropto, output=False, cutoff=None*)

**returns** [GEO or DSM](image_classes.md) object instance, single channel netcdf files will be read into DSMs, multiple wavelength netcdf files will be read to GEO objects.

- **Parameters:**
    - filename - Path of the NetCDF file.
    - cropto - A geoJSON-type shapefile to crop the input image as it is read in, or a list of the min/max values for latitude and longitude. Format expected is `[min longitude, min latitude, max longitude, max latitude]`. 
    - output - Path to print out the Spectral Data as a geotif (defaults to `False`, no output)
	- cutoff - An optional percentile threshold (0–1) for clipping high values in grayscale bands (e.g., to remove noise from power lines or bright artifacts). Values above this percentile are set to 0. Default is None.

- **Context:**
    - It is common for satellite data downloaded from NASA or Copernicus to be in the NetCDF file format. However, this format can be quite variable. Currently, this function is written for the multi-band NASA style of NetCDF output. If additional flexibility is desirable, we encourage people to reach out on [GitHub](https://github.com/danforthcenter/plantcv-geospatial/issues) and collaborate with the PlantCV community to expand our support.
    - Currently we require the use of `cropto`, a shapefile or list of bounding coordinates. This is primarily because the method for calculating the affine transform matrix between array coordinates and geospatial coordinates is impacted by the shape of the Earth if the coverage is too large, as is typical of satellite images. Cropping to a smaller region decreases that effect.

- **Example use:**
    - below

```python
import plantcv.geospatial as gcv

# Read in NetCDF file
nasafile = "./sentinel-3_example.nc"
geo = gcv.read.netcdf(filename=nasafile, cropto="./bigspiritlake.geojson") 

```

![Screenshot](documentation_images/bigspiritlake.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/read.netcdf.py)
