"""Tests for geospatial.convert.points"""

import pytest
import os
import napari
import joblib
from plantcv.geospatial.convert.points import points

# Set up fake class just for testing the annotate output
# Don't want to have to have annotate as a dependency


class FakePoints:
    def __init__(self):
        self.coords = {}


def test_geospatial_points_from_napari_to_geojson_napari(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_points()
    filename = os.path.join(cache_dir, 'test_out.geojson')
    _ = points(source=viewer, dest=filename, img=img)
    assert os.path.exists(filename)


def test_geospatial_points_from_napari_to_geojson_an(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = FakePoints()
    viewer.coords["default"] = []
    filename = os.path.join(cache_dir, 'test_out.geojson')
    _ = points(source=viewer, dest=filename, img=img)
    assert os.path.exists(filename)


def test_geospatial_points_from_napari_to_geojson_badviewer(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = []
    filename = os.path.join(cache_dir, 'test_out.geojson')
    with pytest.raises(RuntimeError):
        _ = points(source=viewer, dest=filename, img=img)


def test_geospatial_points_from_napari_to_geojson_badfilename(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = FakePoints()
    viewer.coords["default"] = []
    filename = os.path.join(cache_dir, 'test_out.txt')
    _ = points(source=viewer, dest=filename, img=img)
    assert os.path.exists(filename + ".geojson")


def test_geospatial_points_from_geojson_to_list(test_data):
    """Test for plantcv-geospatial."""
    l = points(source=test_data.square_crop)
    # this is length 5 because the final point "closes" the polygon
    assert len(l) == 5
