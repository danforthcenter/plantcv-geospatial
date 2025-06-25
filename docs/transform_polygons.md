## Transform Polygons

Transform the points from a polygon or multi polygon-type georeferenced shapefile/GeoJSON based on an image size. 

**plantcv.geospatial.transform_polygons**(*img, geojson*)

**returns** list of transformed coordinates

- **Parameters:**
    - img - Spectral image object, likely read in with [`read_geotif`](read_geotif.md)
    - geojson - Path to the shapefile/GeoJSON containing the points. Can be Polygon or MultiPolygon geometry.

- **Context:**
    - Transformed points can be used downstream for PlantCV analysis, such as defining ROIs. 
- **Example use:**
    - below to define plot boundaries


```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv

# Read geotif in
spectral = gcv.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
coords = gcv.transform_polygons(img=spectral, geojson="./polygons_example.geojson")
# plot ROI from first shape in list 
roi_objects = pcv.roi.custom(img=spectral.pseudo_rgb, vertices=coords[0])

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/transform_polygons.py)