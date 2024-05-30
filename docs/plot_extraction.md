## Create a rectangular shapefile to extract area of interest from agricultural research plots


**plantcv.geospatial.extract_plot**(*input_filename, output_filename, ranges, columns, length of row, vertical alley, horizontal alley)

**returns** [Multi-Polygon Shapefile]

- **Parameters:**
    - input_filename - Filepath to input shapefile consiting four corners of the field
    - output_filename - Filepath to output shapefile containing individual rectangular ploygon corresponding to specific research plot
    - ranges - Number of ranges
    - columns - Number of columns
    - row_length - Row longth along column in meters
    - vertical_alley - Length of alley between ranges in meters
    - horziontal_alley - Length of alley between columns in meters

- **Example use:**
    - below


```python
import plantcv.plantcv as pcv 
import plantcv.geospatial.extract_plot as gridcell

# Path of input and output shapefile
input_shapefile_path = '712_corner_points.shp'
output_shapefile_path = '712_polygon.shp'  
output_shapefile = gridcell.write_shapefile(input_shapefile_path, output_shapefile_path, number_of_ranges=45, number_of_columns=12, 
row_length_along_column=2.4384, vertical_alley=0.9144, 
horizontal_alley=0.03048)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/plot_extract.py)
