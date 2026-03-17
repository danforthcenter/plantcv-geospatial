## Convert Shapes between geojson and lists

Using a Napari or PlantCV-annotate viewer object with clicked polygons, output a shapefile.

**plantcv.geospatial.convert.points**(*img, source, dest=None, shapetype="polygon", layername="Shapes"*)

- **Parameters:**
    - img - Spectral image object, likely read in with [`geo.read_geotif`](read_geotif.md). If `source` is the path to a shapefile, the metadata of this image will be used to convert points to numpy coordinates.
    - source - str or Napari.viewer. If this is an str then it should be a path to a geojson file to read points from. A Napari.viewer should have a polygon like layer that will be saved to a geojson specified by `dest`.
	- dest - str, Path to save a geojson file if `source` is a Napari.viewer. This is not required if `source` is a geojson file path.
    - shapetype - str, Geometry type from Napari viewer shape layer to be written to geojson output. Only used if `source` is a viewer. 
    - layername - str, Name of the shapes layer in the napari viewer. Only used if `source` is a viewer.


- **Context:**
    - Convert points to/from coordinates and geojson files.
- **Example use:**
    - below to click plant locations


```python
import plantcv.geospatial as gcv
import plantcv.annotate as an

# Read geotif in
img = gcv.read_geotif("../read_geotif/rgb.tif", bands="R,G,B")
viewer = an.napari_open(img=img.pseudo_rgb)
viewer.add_shapes()

# A napari viewer window will pop up, use the points function to add clicks
```
```python
# In a separate cell, save the output after clicking:
gcv.convert.shapes(img=img, source=viewer, dest="./points_example.geojson")
```

![Screenshot](documentation_images/napari_clicks.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/convert/shapes.py)
