## Create a grid of cells and save them to a new GeoJSON

**geospatial.create_grid_cells**(*four_points_path, out_path, alley_size, num_ranges, num_plots,
                      row_per_plot=4, vertical_length=3.6576, horizontal_length=0.9144*)

**returns** list of cells

- **Parameters:**
    - four_points_path - Path to GeoJSON/shapefile containing four corner points (used to determine polygon directions, and the output CRS)
    - out_path - Path to save the geojson shapefile. Should be ".geojson" file type. 
    - alley_size - Size of alley spaces beteen ranges
    - num_ranges - Number of ranges
    - num_plots - Number of plots
    - row_per_plot - Number of equidistant rows within a single plot, default: 4
    - vertical_length - Length of each grid cell, default: 3.6576m (7 feet), in units matching the coordinate system of the `four_points_path`
    - horizontal_length - Width of each grid cell, default: 0.9144m (30 inches), in units matching the coordinate system of the `four_points_path`

- **Context:**
    - Helpful for precision planters without GPS

- **Example use:**
    - below


```python
import plantcv.geospatial as geo

gridcells = geo.create_grid_cells(four_points_path="bounds.geojson", 
                    out_path="gridcells.geojson", alley_size=1.5, num_ranges=22, num_plots=13,
                    row_per_plot=4, vertical_length=2.5, horizontal_length=1.6)

```
**Example GeoJSON inputs and output**

![Screenshot](documentation_images/)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/create_grid_cells.py)
