"""Tests for geospatial.transform_points"""

from plantcv.geospatial.create_shapes import auto_grid
import pytest
import dill as pickle
import os


def test_geospatial_shape_auto_grid(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    # Read in test data
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    _ = auto_grid(img=img, field_corners_path=test_data.point_crop, out_path=filename, num_ranges=2, num_columns=16,
             num_rows=4, range_length=3.6576, row_length=0.9144, range_spacing=0, column_spacing=0)
    assert os.path.exists(filename)


def test_geospatial_shape_auto_grid_None(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    with pytest.raises(RuntimeError):
        _ = auto_grid(img=img, field_corners_path=test_data.point_crop, out_path="file.geojson")
