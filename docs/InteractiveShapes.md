## class InteractiveShapes

A PlantCV-Geospatial data object class.

*class* plantcv.geospatial.**InteractiveShapes**

`InteractiveShapes` is a class that is used to create instances of interactive image viewers. Users can use layers of the viewer to manually create plot boundaries. Interactive viewers are useful for field layouts involving individual plants in rough but imperfect grids. 
Methods using `InteractiveShapes` objects can automatically draw lines separating plots, which can be manually corrected before using the lines to draw plot boundary polygons, which can again be manually corrected before saving as a shapefile.  

### Attributes

Attributes are accessed as interactive_shapes_instance.*attribute*.

**viewer**: An interactive viewer object. 

**viewer_type**: Type of interactive viewer. Currently, only "napari" is supported. 

**layer_dict**: Dictionary of layer names in the viewer. Keys represent commonly used shapes important for methods of this class. Notably, "field_boundary" denotes a polygon encompassing the entire field, "grid_lines_columns" denotes lines separating columns of plots, "grid_lines_ranges" denotes lines separating ranges of plots, and "plot_polygons" denotes individual plot polygons. 

### Methods with examples

```python
import plantcv.geospatial as gcv
import plantcv.plantcv as pcv
# Adjust line thickness (default is 5)
pcv.params.line_thickness = 8

# Initialize an InteractiveShapes class object 
# and add an image layer and field boundary layer to the viewer
editor = InteractiveShapes(img, field_layer="field_boundary")

# After drawing a polygon around the field in the "field_boundary" layer, 
# automatically draw a grid of lines
# Uses layer_dict["field_boundary"] to find layer containing field outline
editor.grid(numdivs=[3,4])

# After correcting lines until they enclose individual plots, 
# draw polygons using the line intersections
# Uses layer_dict["grid_lines_columns"] and layer_dict["grid_lines_ranges"] 
# to find layers containing lines
editor.plots()

# Individual plot boundaries can then be saved to a file
gcv.convert.shapes_to_geojson(img, viewer=editor.viewer, out_path="./plots.geojson",
                                layername=editor.layer_dict["plot_polygons"])

# Custom layers can be added for other more manual shape creation
editor.add_layer(layer_type="shapes")
```

**Adding field polygon to shapes layer:**

![Screenshot](documentation_images/field_polygon.png)

**After adjusting position of grid lines:**

![Screenshot](documentation_images/grid_lines.png)

**After adjusting vertices of grid polygons:**

![Screenshot](documentation_images/grid_polygons.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-geospatial/blob/main/plantcv/geospatial/classes.py)
