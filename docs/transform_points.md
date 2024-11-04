## Transform Points

Transform the points from a georeferenced shapefile/GeoJSON based on an image size. 

**plantcv.geospatial.transform_points**(*img, geojson*)

**returns** list of transformed coordinates

- **Parameters:**
    - img - Spectral image object, likely read in with [`geo.read_geotif`](read_geotif.md)
    - geojson - Path to the shapefile/GeoJSON containing the points. Can be Point or MultiPoint geometry.

- **Context:**
    - Transformed points can be used downstream for Python analysis, such as defining ROIs. 
- **Example use:**
    - below to define plot boundaries


```python
import plantcv.geospatial as geo

# Read geotif in
spectral = geo.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
coords = geo.transform_points(img=spectral, geojson="./experimental_bounds_2024.shp")
roi_objects = pcv.roi.custom(img=spectral.pseudo_rgb, vertices=coords)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/transform_points.py)
