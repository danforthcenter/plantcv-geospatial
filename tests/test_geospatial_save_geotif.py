"""Tests for geospatial.save_geotif."""

import os
import plantcv.plantcv as pcv
from plantcv.geospatial import save_geotif, read_geotif


def test_save_geotif_color(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # Create test image
    img = read_geotif(filename=test_data.cropped_tif, bands="B,G,R,RE,N")
    filename = os.path.join(cache_dir, 'test.tif')
    save_geotif(out_img=img.array_data, in_img=img, out_path=filename)
    # Assert that the file was created
    assert os.path.exists(filename)


def test_save_geotif_binary(test_data, tmpdir):
    """Test for PlantCV."""
    # Create a test tmp directory
    cache_dir = tmpdir.mkdir("cache")
    # Create test image
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    gray = pcv.rgb2gray_hsv(rgb_img=img.pseudo_rgb, channel="s")
    thresh = pcv.threshold.binary(gray_img=gray, threshold=60, object_type="light")
    filename = os.path.join(cache_dir, 'test_binary.tif')
    save_geotif(out_img=thresh, in_img=img, out_path=filename)
    # Assert that the file was created
    assert os.path.exists(filename)
