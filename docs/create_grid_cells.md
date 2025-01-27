## Create a grid of cells from input points GeoJSON and save them to a new GeoJSON

**geospatial.create_grid_cells**(*four_points_path, plot_shapefile_path, out_path,
horizontal_cells=8, vertical_length=3.6576, horizontal_length=0.9144*)

- **Parameters:**
    - four_points_path - Path to GeoJSON/shapefile containing four corner points (used to determine polygon directions)
    - plot_geojson_path - Path to geojson containing plot corner points
    - out_path - Path to save the geojson shapefile. Should be ".geojson" file type. 
    - horizontal_cells - Number of cells to divide the horizontal edge into, default: 8
    - vertical_length - Length of each grid cell, default: 3.6576m (7 feet)
    - horizontal_length - Width of each grid cell, default: 0.9144m (30 inches)

- **Context:**
    - 
- **Example use:**
    - below


```python
import plantcv.geospatial as geo

gridcells = geo.create_grid_cells**(four_points_path="plot_bounds.geojson", 
                    plot_shapefile_path="grid_corners.geojson", 
                    out_path="gridcells.geojson", horizontal_cells=8, 
                    vertical_length=3.6576, horizontal_length=0.9144)

```

![Screenshot](documentation_images/

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/create_grid_cells.py)