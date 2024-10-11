"""Tests for geospatial.points_to_geojson"""

import pytest
import os
import napari
from plantcv.geospatial import read_geotif
from plantcv.geospatial import points_to_geojson

# Set up fake class just for testing the annotate output
# Don't want to have to have annotate as a dependency

class FakePoints:
    def __init__(self):
        self.coords = {}

def test_geospatial_points_to_geojson_napari(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_points()
    filename = os.path.join(cache_dir, 'test_out.geojson')
    points_to_geojson(img, viewer, output=filename)
    assert os.path.exists(filename)

def test_geospatial_points_to_geojson_an(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    viewer = FakePoints()
    viewer.coords["default"] = []
    filename = os.path.join(cache_dir, 'test_out.geojson')
    points_to_geojson(img, viewer, output=filename)
    assert os.path.exists(filename)

def test_geospatial_points_to_geojson_badviewer(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    viewer = []
    filename = os.path.join(cache_dir, 'test_out.geojson')
    with pytest.raises(RuntimeError):
        points_to_geojson(img, viewer, output=filename)
