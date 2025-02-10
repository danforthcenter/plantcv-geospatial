## Screenshot a Napari window with plotted shapes from a shapefile

Visualization of shapes from a shapefile by plotting in a Napari window.  

**plantcv.geospatial.visualize.napari_screenshot**(*img, geojson, shape_type="polygon"*)

**returns** Image from the Napari window screenshot

- **Parameters:**
    - img - Spectral image object, likely read in with [`geo.read_geotif`](read_geotif.md)
    - geojson - Path to the shapefile/GeoJSON containing the shapes to be plotted.
    - shape_type - Type of shape contained in geojson. Defaults to "polygon". 

- **Context:**
    - This function plots shapes from a shapefile in a Napari window and then takes a screenshot so that the position of shapes can be easily visualized. 
    - The goal of this function is to enable visualization of shapefiles without opening them in another program.

- **Example use:**
    - Below:

```python
import plantcv.geospatial as geo
import plantcv.plantcv as pcv

pcv.params.debug = "plot"

# Read geotif in
ortho1 = geo.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
 
# Analyze coverage for each region in the geojson
screenshot = geo.visualize.napari_screenshot(img=ortho1,
                           geojson="./shapefiles/experimental_plots.geojson")


```
![Screenshot](documentation_images/analyze_coverage.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/analyze/coverage.py)
