"""Tests for geospatial.transform_points"""

from plantcv.geospatial.shapes import grid as shape_grid
import os


def test_geospatial_shape_grid(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = shape_grid(field_corners=test_data.point_crop, out_path=filename, alley_size=0, num_ranges=2, num_columns=16,
                       num_rows=4, range_length=3.6576, column_length=0.9144)
    assert len(cells) == 128  # 4 points in plot_geojson_path * 8 cells per point * 4 subcells per cell
