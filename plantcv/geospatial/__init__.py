from importlib.metadata import version
from plantcv.geospatial.read_geotif import read_geotif
from plantcv.geospatial.transform_points import transform_points
from plantcv.geospatial.transform_polygons import transform_polygons
from plantcv.geospatial import convert
from plantcv.geospatial import analyze
from plantcv.geospatial import shapes
from plantcv.geospatial.napari_grid import napari_grid
from plantcv.geospatial.napari_polygon_grid import napari_polygon_grid
from plantcv.geospatial.center_grid_rois import center_grid_rois
from plantcv.geospatial.read_netcdf import read_netcdf
from plantcv.geospatial.split_rgb_channels import split_rgb_channels
from plantcv.geospatial.rgb_index import rgb_index, list_rgb_indices

# Auto versioning
__version__ = version("plantcv-geospatial")

__all__ = [
    "read_geotif",
    "transform_points",
    "transform_polygons",
    "analyze",
    "shapes",
    "napari_grid",
    "napari_polygon_grid",
    "center_grid_rois",
    "read_netcdf",
    "split_rgb_channels",
    "rgb_index",
    "list_rgb_indices",
    "convert"
]
