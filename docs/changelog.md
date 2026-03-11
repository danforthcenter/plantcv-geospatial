## Changelog

All notable changes to this project will be documented below.

#### geospatial.analyze.color

* v0.1dev: **plantcv.geospatial.analyze.color**(*img, bin_mask, geojson, bins=10, colorspaces="hsv", label=None*)

#### geospatial.analyze.coverage

* v0.1dev: **geospatial.analyze.coverage**(*img, bin_mask, geojson*)

#### geospatial.analyze.height_percentile

* v0.1dev: **geospatial.analyze.height_percentile**(*dsm, geojson, lower=25, upper=90, label=None*)

#### geospatial.analyze.spectral_index

* v0.1dev: **geospatial.analyze.spectral_index**(*img, geojson, percentiles=None, label=None*)
#### geospatial.analyze.height_subtraction

* v0.1dev: **geospatial.analyze.height_subtraction**(*dsm1, dsm0*)

#### geospatial.convert.points_to_roi_circle

* v0.1dev: rois = **geospatial.convert.points_to_roi_circle**(*img, geojson, radius*)

#### geospatial.convert.points_to_geojson

* v0.1dev: **geospatial.convert.points_to_geojson**(*img, viewer, out_path*)

#### geospatial.convert.shapes_to_geojson

* v0.1dev: coord = **geospatial.convert.shapes_to_geojson**(*img, viewer, out_path, layername="Shapes"*)

#### geospatial.center_grid_rois

* v0.1dev: rois = **geospatial.center_grid_rois**(*img, viewer, radius=10, layername="Shapes"*)

#### geospatial.napari_polygon_grid

* v0.1dev: **geospatial.napari_polygon_grid**(*viewer, layername="Shapes"*)

#### geospatial.read.geotif

* v0.1dev: spectral = **geospatial.read.geotif**(*filename, bands="B,G,R", cropto=None, cutoff=None*)

#### geospatial.read.netcdf

* v0.1dev: spectral = **geospatial.read.netcdf**(*filename, cropto, output=False*)

#### geospatial.create_shapes.grid

* v0.1dev: cells = **geospatial.create_shapes.grid**(*img, field_corners_path, out_path, num_ranges, num_columns,
         range_length, row_length, num_rows=1, range_spacing=0, column_spacing=0*)

#### geospatial.create_shapes.grid_from_coords

* v0.1dev: cells = **geospatial.create_shapes.grid_from_coords**(*img, field_corners_path, plot_geojson_path, out_path, range_length, row_length, num_rows=1*)

#### geospatial.create_shapes.napari_grid

* v0.1dev: **geospatial.create_shapes.napari_grid**(*viewer, numdivs, layername="Shapes"*)

#### geospatial.create_shapes.napari_polygon_grid

* v0.1dev: **geospatial.create_shapes.napari_polygon_grid**(*viewer, layername="Shapes"*)

#### geospatial.transform_points

* v0.1dev: coord = **geospatial.transform_points**(*img, geojson*)

#### geospatial.transform_polygons

* v0.1dev: coord = **geospatial.transform_polygons**(*img, geojson*)
