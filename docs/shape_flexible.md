## Create cells from input points GeoJSON and save them to a new GeoJSON

**geospatial.shape.flexible**(*field_corners, plot_geojson_path, out_path,
                    num_rows=8, range_length=3.6576, column_length=0.9144*)

**returns** list of cells

- **Parameters:**
    - field_corners - Path to GeoJSON/shapefile containing four corner points (used to determine polygon directions)
    - plot_geojson_path - Path to geojson containing plot corner points
    - out_path - Path to save the geojson shapefile. Should be ".geojson" file type. 
    - num_rows - Number of rows per plot, default: 8
    - range_length - Vertical dimension of each plot, default: 3.6576m (7 feet)
    - column_length - Horizontal dimension of each plot, default: 0.9144m (30 inches)

- **Context:**
    - Helpful for precision planters without GPS

- **Example use:**
    - below


```python
import plantcv.geospatial as geo

gridcells = geo.shape.flexible(field_corners="bounds.geojson",
                plot_geojson_path="plot_points.geojson",
                out_path="gridcells.geojson", num_rows=8, 
                range_length=3.6576, column_length=0.9144)

```
**Example GeoJSON inputs and output**

`field_corners` here is represented with yellow points, `plot_geojson_path` with white points, and the resulting `plot_shapefile_path="gridcells.geojson"` is shown in red. Note that the `plot_shapefile_path` points are in the bottom right corner of each grid cell, so the `four_points_path` points are collected starting in the bottom right corner and moving clockwise. 

![Screenshot](documentation_images/irregular_grid_cells.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/create_grid_cells.py)
