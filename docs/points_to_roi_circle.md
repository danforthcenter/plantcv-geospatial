## Create Circular ROIs from georeferenced points

Transform the points from a Points-type georeferenced shapefile/GeoJSON into circular Regions of Interest (ROIs) and save the shapefile/GeoJSON with points added.

**plantcv.geospatial.convert.points_to_roi_circle**(*img, geojson, radius*)

**returns** list of ROIs (`plantcv.Objects` instance)

- **Parameters:**
    - img - Spectral image object, likely read in with [`geo.read_geotif`](read_geotif.md)
    - geojson - Path to the shapefile/GeoJSON containing the points.
    - radius - Radius of circular ROIs to get created,
                in units matching the coordinate system of the image

- **Context:**
    - Directly create ROIs with a consistent georeferenced radius
- **Example use:**
    - below


```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv

# Read geotif in
spectral = gcv.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
rois = gcv.convert.points_to_roi_circle(img=spectral, geojson="./points_example.geojson", radius=1)
# Segmentation steps here
masks = []
for roi in rois:  # PlantCV ROI tools generally expect one ROI at a time.
    masks.append(pcv.roi.quick_filter(mask=vegetation_mask, roi=roi, roi_type="partial"))

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/convert/points_to_roi.py)
