## Create a grid of cells and save them to a new GeoJSON/Shapefile

**geospatial.shapes.grid**(*field_corners, out_path, num_ranges, num_columns, num_rows=4, range_length=3.6576, column_length=0.9144, range_spacing=0, column_spacing=0*)

**returns** list of cells

- **Parameters:**
    - field_corners - Path to GeoJSON/shapefile containing four corner points (used to determine polygon directions, and the output CRS)
    - out_path - Path to save the geojson shapefile. Should be ".geojson" file type. 
    - num_ranges - Number of ranges to get created
    - num_columns - Number of columns to get created
    - num_rows - Number of rows within a single plot, default: 4
    - range_length - Length of each grid cell in the horizontal direction, default: 3.6576 (7 feet in meters), in units matching the coordinate system of the `field_corners`
    - column_length - Length of each grid cell in the vertical direction, default: 0.9144 (30 inches in meters), in units matching the coordinate system of the `field_corners`
    - range_spacing - Length of "alley" spaces between ranges, default: 0
    - column_spacing - Length of "alley" spaces between columns, default: 0

- **Context:**
    - Helpful for precision planters without GPS

- **Example use:**
    - below


```python
import plantcv.geospatial as geo

gridcells = geo.shapes.grid(four_points_path="bounds.geojson", 
                out_path="gridcells.geojson", alley_size=1.5, num_ranges=22, num_plots=13,
                row_per_plot=4, vertical_length=2.5, horizontal_length=1.6)

```
**Example GeoJSON inputs and output**

![Screenshot](documentation_images/)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/shapes.grid.py)
