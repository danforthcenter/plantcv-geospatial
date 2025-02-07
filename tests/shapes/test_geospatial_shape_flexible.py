"""Tests for geospatial.transform_points"""

from plantcv.geospatial.shapes import flexible as shape_flexible
import os


def test_geospatial_shape_flexible(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = shape_flexible(field_corners=test_data.plot_bounds, plot_geojson_path=test_data.plot_points, out_path=filename,
                           num_rows=8, range_length=4, column_length=0.5)
    assert len(cells) == 32   # 4 corner points per cell * 8 cells
    assert os.path.exists(filename)


def test_geospatial_shape_flexible_single_points(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = shape_flexible(field_corners=test_data.point_crop, plot_geojson_path=test_data.plot_points, out_path=filename,
                           num_rows=8, range_length=4, column_length=0.5)
    assert len(cells) == 32 
    assert os.path.exists(filename)
