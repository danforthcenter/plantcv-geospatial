from importlib.metadata import version
from plantcv.geospatial._globals import Field_layout

# Initialize an instance of Field_layout class with default values
# Field_layout is available when PlantCV-Geospatial is imported

field_layout = Field_layout()

from plantcv.geospatial.transform_polygons import transform_polygons
from plantcv.geospatial import read
from plantcv.geospatial import convert
from plantcv.geospatial import analyze
from plantcv.geospatial import create_shapes
from plantcv.geospatial.center_grid_rois import center_grid_rois

# Auto versioning
__version__ = version("plantcv-geospatial")

__all__ = [
    "Field_layout",
    "transform_polygons",
    "read",
    "analyze",
    "create_shapes",
    "center_grid_rois",
    "convert"
]
