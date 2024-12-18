## Create Circular ROIs from georeferenced points

Transform the points from a Points-type georeferenced shapefile/GeoJSON into circular Regions of Interest (ROIs). 

**plantcv.geospatial.points2roi_circle**(*img, geojson, radius*)

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
import plantcv.geospatial as geo
import plantcv.plantcv as pcv

# Read geotif in
spectral = geo.read_geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
rois = geo.points2roi_circle(img=spectral, geojson="./points_example.geojson", radius=1)
# Segmentation steps here
labeled_mask = pcv.roi.filter(mask=vegetation_mask, roi=rois, roi_type="partial")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/points2roi.py)
