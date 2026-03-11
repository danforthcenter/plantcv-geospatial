"""Tests for geospatial.create_shapes.grid_from_coords"""

from plantcv.geospatial.create_shapes import grid_from_coords
from plantcv.plantcv import params
import pytest
import joblib
import os


@pytest.mark.parametrize("debug", ["print", "plot", None])
def test_geospatial_shape_grid_from_coords(debug, test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    # Debug mode
    params.debug = debug
    _ = grid_from_coords(img=img, field_corners_path=test_data.plot_bounds, plot_geojson_path=test_data.plot_points,
                         out_path=filename, num_rows=8, range_length=4, row_length=0.5)
    assert os.path.exists(filename)


def test_geospatial_shape_grid_from_coords_single_points(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    _ = grid_from_coords(img=img, field_corners_path=test_data.point_crop, plot_geojson_path=test_data.plot_points,
                 out_path=filename, num_rows=8, range_length=4, row_length=0.5)
    assert os.path.exists(filename)
