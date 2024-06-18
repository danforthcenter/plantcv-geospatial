from importlib.metadata import version
from plantcv.geospatial.read_geotif import read_geotif

# Auto versioning
__version__ = version("plantcv-geospatial")

__all__ = [
    "read_geotif"
    "plot_extraction"
    ]
