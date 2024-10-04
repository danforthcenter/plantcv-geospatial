"""Tests for geospatial.points_to_geojson"""

import pytest
import plantcv.annotate as an
from plantcv.geospatial import read_geotif
from plantcv.geospatial import points_to_geojson

def test_geospatial_points_to_geojson_napari(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    viewer = an.napari_open(img=img.pseudo_rgb, show=False)
    viewer.add_points()
    filename = os.path.join(cache_dir, 'test_out.geojson')
    points_to_geojson(img, viewer, output=filename)
    assert os.path.exists(filename)

def test_geospatial_points_to_geojson_an(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    viewer = an.Points(img=img.pseudo_rgb)
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
