"""Tests for geospatial.shapes_to_geojson"""

import os
import napari
import joblib
from plantcv.geospatial import shapes_to_geojson


def test_geospatial_points_to_geojson_napari(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes([[2, 3], [3, 3], [3, 4], [2, 4]], shape_type="polygon")
    filename = os.path.join(cache_dir, 'test_out.geojson')
    shapes_to_geojson(img, viewer, out_path=filename)
    assert os.path.exists(filename)
