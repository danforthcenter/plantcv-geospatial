## Create a grid of cells from input points GeoJSON and save them to a new GeoJSON

**geospatial.create_polygons**(*four_points_path, plot_geojson_path, out_path,
horizontal_cells=8, vertical_length=3.6576, horizontal_length=0.9144*)

- **Parameters:**
    - four_points_path - Path to GeoJSON/shapefile containing four corner points (used to determine polygon directions)
    - plot_geojson_path - Path to geojson containing plot corner points
    - out_path - Path to save the geojson shapefile. Should be ".geojson" file type. 
    - horizontal_cells - Number of cells to divide the horizontal edge into, default: 8
    - vertical_length - Length of each grid cell, default: 3.6576m (7 feet)
    - horizontal_length - Width of each grid cell, default: 0.9144m (30 inches)

- **Context:**
    - Helpful for precision planters without GPS

- **Example use:**
    - below


```python
import plantcv.geospatial as geo

gridcells = geo.create_polygons(four_points_path="bounds.geojson", 
                    plot_geojson_path="plot_points.geojson", 
                    out_path="gridcells.geojson", horizontal_cells=8, 
                    vertical_length=3.6576, horizontal_length=0.9144)

```
**Example GeoJSON inputs and output**

`four_points_path` here is represented with yellow points, `plot_geojson_path` with white points, and the resulting `plot_shapefile_path="gridcells.geojson"` is shown in red. Note that the `plot_shapefile_path` points are in the bottom right corner of each grid cell, so the `four_points_path` points are collected starting in the bottom right corner and moving clockwise. 

![Screenshot](documentation_images/irregular_grid_cells.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/create_grid_cells.py)
