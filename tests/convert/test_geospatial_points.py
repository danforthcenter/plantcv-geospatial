"""Tests for geospatial.convert.points"""

import pytest
import os
import napari
import dill as pickle
from plantcv.geospatial.convert.points import points

# Set up fake class just for testing the annotate output
# Don't want to have to have annotate as a dependency


class FakePoints:
    def __init__(self):
        self.coords = {}


def test_geospatial_points_from_napari_to_geojson_napari(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_points()
    filename = os.path.join(cache_dir, 'test_out.geojson')
    _ = points(img=img, source=viewer, dest=filename)
    assert os.path.exists(filename)


def test_geospatial_points_from_napari_to_geojson_an(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    viewer = FakePoints()
    viewer.coords["default"] = []
    filename = os.path.join(cache_dir, 'test_out.geojson')
    _ = points(img=img, source=viewer, dest=filename)
    assert os.path.exists(filename)


def test_geospatial_points_from_napari_to_geojson_badviewer(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    viewer = []
    filename = os.path.join(cache_dir, 'test_out.geojson')
    with pytest.raises(RuntimeError):
        _ = points(img=img, source=viewer, dest=filename)


def test_geospatial_points_from_napari_to_geojson_badfilename(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    viewer = FakePoints()
    viewer.coords["default"] = []
    filename = os.path.join(cache_dir, 'test_out.txt')
    _ = points(img=img, source=viewer, dest=filename)
    assert os.path.exists(filename + ".geojson")


def test_geospatial_points_from_geojson(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    coords = points(img=img, source=test_data.pts_geojson)
    assert len(coords) == 4


def test_geospatial_single_points_from_geojson(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    coords = points(img=img, source=test_data.single_pts_geojson)
    assert len(coords) == 8
