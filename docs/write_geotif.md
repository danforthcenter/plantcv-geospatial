## Save GeoTIFF data

Save out a new or modified data array to a GeoTIFF file. 

**geospatial.write_geotif**(*path, img, transform=None, crs=None, nodata=None*)

- **Parameters:**
    - path - Path and filename for saving the new GeoTIFF.
    - img - Either a numpy array, [GEO or DSM](image_classes.md) object containing data to be saved.
        If a GEO or DSM object is used then the `transform` and `crs` attributes of that object are used by default.
    - transform - Affine transformation matrix that converts array coordinates to geospatial coordinates.
    - crs - Coordinate reference system.
    - nodata - No data value.

- **Context:**
    - This function is useful for saving modified geospatial objects as new files after [resizing](resize.md) or georeferencing. 

- **Example use:**

```python
import plantcv.geospatial as gcv

# Read geotif in
ortho = gcv.read.geotif(filename="./data/example_img.tif", bands="B,G,R,RE,NIR")
resized = gcv.resize(img=ortho, size=(2000, 2000))
gcv.write_geotif(path="./outputs/resized_img.tif", img=resized)


```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/write_geotif.py)
