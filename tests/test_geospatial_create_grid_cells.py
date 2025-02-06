"""Tests for geospatial.transform_points"""

from plantcv.geospatial import create_polygons, create_grid_cells
import os


def test_geospatial_create_polygons(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = create_polygons(four_points_path=test_data.plot_bounds, plot_geojson_path=test_data.plot_points, out_path=filename,
                            horizontal_cells=8, vertical_length=4, horizontal_length=0.5)
    assert len(cells) == 32   # 4 corner points per cell * 8 cells
    assert os.path.exists(filename)


def test_geospatial_create_polygons_single_points(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = create_polygons(four_points_path=test_data.point_crop, plot_geojson_path=test_data.plot_points, out_path=filename,
                            horizontal_cells=8, vertical_length=4, horizontal_length=0.5)
    assert len(cells) == 32 
    assert os.path.exists(filename)


def test_geospatial_create_grid_cells(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    cells = create_grid_cells(four_points_path=test_data.point_crop, out_path=filename, alley_size=0,
                              num_ranges=2, num_plots=16,
                              row_per_plot=4, vertical_length=3.6576, horizontal_length=0.9144)
    assert len(cells) == 128  # 4 points in plot_geojson_path * 8 cells per point * 4 subcells per cell

