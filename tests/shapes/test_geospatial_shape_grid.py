"""Tests for geospatial.transform_points"""

from plantcv.geospatial.shapes import grid as shape_grid
import joblib
import os


def test_geospatial_shape_grid(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    # Read in test data
    img = joblib.load(test_data.rgb_pickled)
    _ = shape_grid(img=img, field_corners_path=test_data.point_crop, out_path=filename, num_ranges=2, num_columns=16,
                   num_rows=4, range_length=3.6576, row_length=0.9144, range_spacing=0, column_spacing=0)
    assert os.path.exists(filename)
