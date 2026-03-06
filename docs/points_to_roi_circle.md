## Create Circular ROIs from georeferenced points

Transform the points from a Points-type georeferenced shapefile/GeoJSON into circular Regions of Interest (ROIs) and save the shapefile/GeoJSON with points added to the `geojson` path with `_circles.geojson` appended to the extensionless basename.

**plantcv.geospatial.convert.points_to_roi_circle**(*img, geojson, radius*)

**returns** list of ROIs (`plantcv.Objects` instance)

- **Parameters:**
    - img - Spectral image object, likely read in with [`geo.read_geotif`](read_geotif.md)
    - geojson - Path to the shapefile/GeoJSON containing the points.
    - radius - Radius of circular ROIs to get created,
                in units matching the coordinate system of the image

- **Context:**
    - Directly create ROIs with a consistent georeferenced radius and write geojson of ROIs.
- **Example use:**
    - below


```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv

# Read geotif in
spectral = gcv.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
rois = gcv.convert.points_to_roi_circle(img=spectral, geojson="./points_example.geojson", radius=1)
# "./points_example_circles.geojson" file can be used for gcv.analyze functions
res = gcv.analyze.height_percentile(img=spectral, geojson="./points_example_circles.geojson")
# Segmentation steps here
pcv.roi.quick_filter(mask=vegetation_mask, roi=roi, roi_type="partial")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/convert/points_to_roi.py)
