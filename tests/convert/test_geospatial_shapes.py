"""Tests for geospatial.convert.shapes"""

import os
import napari
import dill as pickle
from plantcv.geospatial.convert.shapes import shapes


def test_geospatial_shapes_from_napari_to_geojson(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.thumb)
    viewer.add_shapes([[2, 3], [3, 3], [3, 4], [2, 4]], shape_type="polygon")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    _ = shapes(img=img, source=viewer, dest=filename)
    assert os.path.exists(filename)


def test_geospatial_shapes_to_geojson_badfilename(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.thumb)
    viewer.add_shapes([[2, 3], [3, 3], [3, 4], [2, 4]], shape_type="polygon")
    filename = os.path.join(cache_dir, 'test_out.txt')
    _ = shapes(img=img, source=viewer, dest=filename)
    assert os.path.exists(filename + ".geojson")


def test_geospatial_shapes_from_geojson_to_list(test_data):
    """Test for plantcv-geospatial."""
    with open(test_data.geo_pickled, "rb") as f:
        img = pickle.load(f)
    l = shapes(img=img, source=test_data.square_crop)
    assert len(l[0]) == 4
