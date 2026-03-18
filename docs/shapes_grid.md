## Automatically create a grid of cells from a field layout

**plantcv.geospatial.create_shapes.auto_grid**(*img, field_corners_path, out_path, num_ranges=field_layout.num_ranges, num_columns=field_layout.num_columns, range_length=field_layout.range_length, row_length=field_layout.row_length, num_rows=field_layout.num_rows, range_spacing=field_layout.range_spacing, column_spacing=field_layout.column_spacing, ids=None*)

**returns** figure

- **Parameters:**
    - img - Spectral_Data object of geotif data, used for plotting a debug image, likely read in with [`read.geotif`](read_geotif.md)
    - field_corners_path - Path to GeoJSON/shapefile containing four corner points (used to determine polygon directions, and the output CRS)
    - out_path - Path to save the geojson shapefile. Should be ".geojson" file type. 
    - num_ranges - Number of ranges to get created. Defaults to the `num_ranges` attribute of the `Field_layout` class. 
    - num_columns - Number of columns to get created. Defaults to the `num_columns` attribute of the `Field_layout` class. 
    - range_length - Length of each grid cell in the horizontal direction, in units matching the coordinate system of the `field_corners_path`. Defaults to the `range_length` attribute of the `Field_layout` class. 
    - row_length - Length of each grid cell in the vertical direction, in units matching the coordinate system of the `field_corners_path`. Defaults to the `row_length` attribute of the `Field_layout` class. 
    - num_rows - Number of rows within a single plot. Defaults to the `num_rows` attribute of the `Field_layout` class. 
    - range_spacing - Length of "alley" spaces between ranges. Defaults to the `range_spacing` attribute of the `Field_layout` class. 
    - column_spacing - Length of "alley" spaces between columns. Defaults to the `column_spacing` attribute of the `Field_layout` class. 
	- ids - Optional IDs to label the geojson plots.

- **Context:**
    - Helpful for precision planted experiments

![Screenshot](documentation_images/row_plot_vocab.png)


- **Example use:**
    - Example image from the [Bison-Fly: UAV pipeline at NDSU Spring Wheat Breeding Program](https://github.com/filipematias23/Bison-Fly) below. 


```python
import plantcv.geospatial as gcv

# Read geotif in
ortho1 = gcv.read.geotif(filename="./data/example_img.tif", bands="b,g,r,RE,NIR")
# Create and visualize GeoJSON of plots
figure = gcv.create_shapes.auto_grid(img=img, field_corners_path="bounds.geojson", 
            out_path="gridcells.geojson", num_ranges=22, num_columns=13,
            num_rows=1, range_spacing=1.5,  range_length=2.5, row_length=1.6)

```
**Example GeoJSON output figure**

![Screenshot](documentation_images/grid_cells.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/create_shapes/auto_grid.py)
