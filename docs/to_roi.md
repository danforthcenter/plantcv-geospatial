## Create Circular ROIs from georeferenced points

Transform features from shapefile/GeoJSON to Regions of Interest (ROIs) and save a shapefile/GeoJSON of those ROIs.

Shapefiles/GeoJSONs will be written with the `_circles` or `_polygons` suffix.

**plantcv.geospatial.convert.to_roi**(*img, geojson, radius=None*)

**returns** list of ROIs (`plantcv.Objects` instance)

- **Parameters:**
    - img - Spectral image object, likely read in with [`geo.read.geotif`](read_geotif.md)
    - geojson - Path to the shapefile/GeoJSON containing the points or polygons.
    - radius - Optional radius of circular ROIs to get created,
                in units matching the coordinate system of the image.
				If this is provided then the geojson is assumed to contain points.

- **Context:**
    - Directly create ROIs with a consistent georeferenced radius and write geojson of ROIs.
- **Example use:**
    - below


```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv

# Read geotif in
spectral = gcv.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
rois = gcv.convert.to_roi(img=spectral, geojson="./points_example.geojson", radius=1)
# "./points_example_circles.geojson" file can be used for gcv.analyze functions
res = gcv.analyze.height_percentile(img=spectral, geojson="./points_example_circles.geojson")
# Segmentation steps here
pcv.roi.quick_filter(mask=vegetation_mask, roi=roi, roi_type="partial")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/convert/to_roi.py)
