"""Tests for geospatial.napari_save_points"""

import os
from plantcv.geospatial import napari_save_points, read_geotif
from plantcv.plantcv import print_image


def test_geospatial_napari_save_points(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    images = [test_data.rgb_tif]
    redo_list = napari_save_points(images, num_points=4, outdir=cache_dir, block=False, show=False) 
    assert len(redo_list) == 1
    viewer.close()


def test_geospatial_napari_save_points_output(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    cache_dir = tmpdir.mkdir("cache")
    # test with a png by creating a temp version of the rgb tif in cache_dir
    img = read_geotif(filename=test_data.rgb_tif, bands="R,G,B")
    print_image(img.pseudo_rgb, os.path.join(cache_dir, "rgb.png"))
    images = [os.path.join(cache_dir, "rgb.png")]
    _ = napari_save_points(images, num_points=0, outdir=cache_dir, block=False, show=False) 
    assert os.path.exists(os.path.join(cache_dir, "rgb_warp.txt"))
    viewer.close()
