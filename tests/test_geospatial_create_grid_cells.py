"""Tests for geospatial.transform_points"""

from plantcv.geospatial import create_grid_cells
import pytest, os


def test_geospatial_transform_points(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = create_grid_cells(four_points_path=test_data.plot_bounds, plot_geojson_path=test_data.plot_points, out_path=filename,
                              horizontal_cells=8, vertical_length=4, horizontal_length=0.5)
    assert len(cells) == 32  # 4 points in plot_geojson_path * 8 cells per point
    assert os.path.exists(filename)
