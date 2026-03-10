"""Tests for geospatial.convert.shapes"""

import os
import napari
import joblib
from plantcv.geospatial.convert.shapes import shapes


def test_geospatial_shapes_from_napari_to_geojson(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes([[2, 3], [3, 3], [3, 4], [2, 4]], shape_type="polygon")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    _ = shapes(frm=viewer, to=filename, img=img)
    assert os.path.exists(filename)


def test_geospatial_shapes_to_geojson_badfilename(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes([[2, 3], [3, 3], [3, 4], [2, 4]], shape_type="polygon")
    filename = os.path.join(cache_dir, 'test_out.txt')
    _ = shapes(frm=viewer, to=filename, img=img)
    assert os.path.exists(filename + ".geojson")


def test_geospatial_shapes_from_geojson_to_list(test_data):
    """Test for plantcv-geospatial."""
    l = shapes(frm=test_data.square_crop)
    # this is length 5 because the final point "closes" the polygon
    assert len(l[0][0]) == 5
