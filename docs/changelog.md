## Changelog

All notable changes to this project will be documented below.

#### geospatial.analyze.color

* v0.1dev: **plantcv.geospatial.analyze.color**(*img, bin_mask, geojson, bins=10, colorspaces="hsv", label=None*)

#### geospatial.analyze.coverage

* v0.1dev: **geospatial.analyze.coverage**(*img, bin_mask, geojson*)

#### geospatial.analyze.height_percentile

* v0.1dev: **geospatial.analyze.height_percentile**(*dsm, geojson, lower=25, upper=90, label=None*)

#### geospatial.analyze.spectral_index

* v0.1dev: **geospatial.analyze.spectral_index**(*img, geojson, index, percentiles=None, label=None, distance=20*)

#### geospatial.analyze.height_subtraction

* v0.1dev: **geospatial.analyze.height_subtraction**(*dsm1, dsm0*)

#### geospatial.center_grid_rois

* v0.1dev: rois = **geospatial.center_grid_rois**(*editor, radius=10, layername="Shapes"*)

#### geospatial.convert.to_roi

* v0.1dev: rois = **geospatial.convert.to_roi**(*img, geojson, radius=None*)

#### geospatial.convert.points

* v0.1dev: **geospatial.convert.points**(*img, source, dest=None, layername="Points"*)

#### geospatial.convert.shapes

* v0.1dev: coord = **geospatial.convert.shapes**(*img, source, dest=None, shapetype="polygon", layername="Shapes"*)

#### geospatial.create_shapes.auto_grid

* v0.1dev: cells = **geospatial.create_shapes.auto_grid**(*img, field_corners_path, out_path, ids=None, \*\*kwargs*)

#### geospatial.create_shapes.grid_from_coords

* v0.1dev: cells = **geospatial.create_shapes.grid_from_coords**(*img, field_corners_path, plot_geojson_path, out_path, ids=None, \*\*kwargs*)

#### geospatial.create_shapes.InteractiveShapes

* v0.1dev: object = **geospatial.create_shapes.InteractiveShapes**(*img, viewer_type="napari", field_layer=None, show=True*)

#### geospatial.create_shapes.InteractiveShapes.add_layer

* v0.1dev: **geospatial.create_shapes.InteractiveShapes.add_layer**(*layer_type="shapes", layername="Shapes"*)

#### geospatial.create_shapes.InteractiveShapes.grid

* v0.1dev: **geospatial.create_shapes.InteractiveShapes.grid**(*numdivs*)

#### geospatial.create_shapes.InteractiveShapes.plots

* v0.1dev: **geospatial.create_shapes.InteractiveShapes.plots**(*plot_layer="Plots"*)

#### geospatial.create_shapes.InteractiveShapes.to_points

* v0.1dev: **geospatial.create_shapes.InteractiveShapes.to_points**(*dest=None, layername="Points"*)

#### geospatial.create_shapes.InteractiveShapes.to_shapes

* v0.1dev: **geospatial.create_shapes.InteractiveShapes.to_shapes**(*dest=None, shapetype="polygon", layername="Shapes"*)

#### geospatial.DSM

* v0.1dev: object = **geospatial.DSM**(*input_array, filename, crs, transform, cutoff*)

#### geospatial.GEO

* v0.1dev: object = **geospatial.GEO**(*input_array, filename, wavelengths, default_wavelengths, crs, transform*)

#### geospatial.Image

* v0.1dev: object = **geospatial.Image**(*input_array, filename*)

#### geospatial.read.geotif

* v0.1dev: geo = **geospatial.read.geotif**(*filename, bands="B,G,R", cropto=None, cutoff=None*)

#### geospatial.read.netcdf

* v0.1dev: geo = **geospatial.read.netcdf**(*filename, cropto, output=False, cutoff=None*)
