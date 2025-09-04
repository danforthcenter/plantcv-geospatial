## Changelog

All notable changes to this project will be documented below.


#### geospatial.analyze.coverage

* v0.1dev: **geospatial.analyze.coverage**(*img, bin_mask, geojson*)

#### geospatial.analyze.height_percentile

* v0.1dev: **geospatial.analyze.height_percentile**(*dsm, geojson, lower=25, upper=90, label=None*)

#### geospatial.analyze.spectral_index

* v0.1dev: **geospatial.analyze.spectral_index**(*img, geojson, percentiles=None, label=None*)

#### geospatial.points2roi_circle

* v0.1dev: rois = **geospatial.points2roi_circle**(*img, geojson, radius*)

#### geospatial.points_to_geojson

* v0.1dev: **geospatial.points_to_geojson**(*img, viewer, out_path*)

#### geospatial.center_grid_rois

* v0.1dev: rois = **geospatial.center_grid_rois**(*img, viewer, radius=10*)

#### geospatial.napari_grid

* v0.1dev: **geospatial.napari_grid**(*viewer, numdivs, layername="Shapes"*)

#### geospatial.napari_polygon_grid

* v0.1dev: **geospatial.napari_polygon_grid**(*viewer*)

#### geospatial.read_geotif

* v0.1dev: spectral = **geospatial.read_geotif**(*filename, bands="B,G,R", cropto=None*)

#### geospatial.read_netcdf

* v0.1dev: spectral = **geospatial.read_netcdf**(*filename, cropto, output=False*)

#### geospatial.shapes.grid

* v0.1dev: cells = **geospatial.shapes.grid**(*img, field_corners_path, out_path, num_ranges, num_columns,
         range_length, row_length, num_rows=1, range_spacing=0, column_spacing=0*)

#### geospatial.shapes.flexible

* v0.1dev: cells = **geospatial.shapes.flexible**(*img, field_corners_path, plot_geojson_path, out_path, range_length, row_length, num_rows=1*)

#### geospatial.transform_points

* v0.1dev: coord = **geospatial.transform_points**(*img, geojson*)

#### geospatial.transform_polygons

* v0.1dev: coord = **geospatial.transform_polygons**(*img, geojson*)

#### geospatial.shapes_to_geojson

* v0.1dev: coord = **geospatial.shapes_to_geojson**(*img, viewer, out_path*)
