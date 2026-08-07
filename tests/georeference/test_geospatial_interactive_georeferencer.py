"""Tests for geospatial.georeference.InteractiveGeoreferencer"""

import os
import shutil
import pytest
import numpy as np
import rasterio
from plantcv.geospatial.georeference.interactive_georeferencer import InteractiveGeoreferencer
from plantcv.geospatial.georeference import _transform_helpers as th

# tests/testdata/small_geotif.tif and small_geotif_no_crs.tif are both this size.
IMG_HEIGHT, IMG_WIDTH = 20, 25


@pytest.mark.parametrize("bad_kwargs", [
    {"mode": "nonsense"},
    {"transform_type": "nonsense"},
    {"mode": "known_coordinates", "known_coords": None},
    {"mode": "reference_image", "reference_image": None},
    {"mode": "known_coordinates", "known_coords": [(0, 0), (1, 0), (0, 1)], "transform_type": "polynomial2"},
])
def test_geospatial_interactive_georeferencer_bad_arguments(bad_kwargs, tmpdir):
    """Test for georeferencer constructor argument checks."""
    img_dir = tmpdir.mkdir("img_dir")
    kwargs = {"img_dir": str(img_dir), "output_dir": str(tmpdir.join("out")), "show": False}
    kwargs.update(bad_kwargs)
    with pytest.raises(RuntimeError):
        _ = InteractiveGeoreferencer(**kwargs)


def test_geospatial_interactive_georeferencer_no_valid_images(tmpdir):
    """Test for georeferencer with no valid images in directory"""
    img_dir = tmpdir.mkdir("img_dir")
    img_dir.join("bad.tif.aux.xml").write("not a real image")
    with pytest.raises(RuntimeError):
        _ = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                     mode="known_coordinates", known_coords=[(0, 0), (1, 0), (0, 1)],
                                     show=False)


def test_geospatial_interactive_georeferencer_known_coordinates_flow(test_data, tmpdir):
    """Test for georeferencer. Full known_coordinates click-through-to-georeference flow,
    across two images, including a rejected (wrong point count) click before the accepted one."""
    img_dir = tmpdir.mkdir("img_dir")
    img1 = str(img_dir.join("img1.tif"))
    img2 = str(img_dir.join("img2.tif"))
    shutil.copy(test_data.small_geotif, img1)
    shutil.copy(test_data.small_geotif, img2)
    known_coords = [(500000.0, 4000000.0), (500100.0, 4000000.0), (500050.0, 4000090.0)]

    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="known_coordinates", known_coords=known_coords,
                                   transform_type="affine", show=False)
    points = np.array([[2.0, 2.0], [2.0, 20.0], [15.0, 10.0]])

    # Wrong point count is rejected without advancing
    geo._points_layer.data = points[:2]
    geo._on_next()
    assert geo.current_index == 0

    # Correct point count advances to image 2
    geo._points_layer.data = points
    geo._on_next()
    assert geo.current_index == 1

    # Correct point count on the last image finishes the queue
    geo._points_layer.data = points
    geo._on_next()
    assert geo.finished

    outputs = geo.georeference()
    assert len(outputs) == 2
    assert geo.crs == "EPSG:32615"
    for out_path in outputs:
        assert os.path.exists(out_path)
        with rasterio.open(out_path) as src:
            assert src.crs == "EPSG:32615"
    geo.close()


def test_geospatial_interactive_georeferencer_known_coordinates_no_crs(test_data, tmpdir):
    """Test for georeferencer with no CRS in first image"""
    img_dir = tmpdir.mkdir("img_dir")
    shutil.copy(test_data.small_geotif_no_crs, str(img_dir.join("img.tif")))
    known_coords = [(500000.0, 4000000.0), (500100.0, 4000000.0), (500050.0, 4000090.0)]
    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="known_coordinates", known_coords=known_coords,
                                   transform_type="affine", show=False)
    geo._points_layer.data = np.array([[2.0, 2.0], [2.0, 20.0], [15.0, 10.0]])
    geo._on_next()
    with pytest.raises(RuntimeError):
        geo.georeference()
    geo.close()


def test_geospatial_interactive_georeferencer_reference_image_flow(test_data, tmpdir):
    """Test for georeferencer with a reference image"""
    ref_path = str(tmpdir.join("ref.tif"))
    shutil.copy(test_data.small_geotif, ref_path)
    img_dir = tmpdir.mkdir("img_dir")
    target1 = str(img_dir.join("target1.tif"))
    target2 = str(img_dir.join("target2.tif"))
    shutil.copy(test_data.small_geotif_no_crs, target1)
    shutil.copy(test_data.small_geotif_no_crs, target2)

    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="reference_image", reference_image=ref_path,
                                   transform_type="affine", show=False)
    assert geo._is_reference == [True, False, False]

    # The reference image can't be skipped
    geo._on_skip()
    assert geo.current_index == 0

    # Too few points on the reference image is rejected without advancing
    geo._points_layer.data = np.array([[3.0, 3.0], [3.0, 20.0]])
    geo._on_next()
    assert geo.current_index == 0
    assert geo.reference_points is None

    # Enough points on the reference image advances to the first target
    geo._points_layer.data = np.array([[3.0, 3.0], [3.0, 20.0], [16.0, 12.0]])
    geo._on_next()
    assert geo.current_index == 1
    assert len(geo.reference_points) == 3

    # Wrong point count on a target image is rejected without advancing
    geo._points_layer.data = np.array([[4.0, 4.0], [4.0, 18.0]])
    geo._on_next()
    assert geo.current_index == 1

    # Matching point count advances to the second target
    geo._points_layer.data = np.array([[4.0, 4.0], [4.0, 18.0], [14.0, 9.0]])
    geo._on_next()
    assert geo.current_index == 2
    assert target1 in geo.gcps

    # Skipping the last (second target) image finishes the queue
    geo._on_skip()
    assert geo.finished
    assert geo.skipped == {target2}

    outputs = geo.georeference()
    assert len(outputs) == 1
    with rasterio.open(outputs[0]) as src:
        assert src.crs == "EPSG:32615"
        assert src.shape == (IMG_HEIGHT, IMG_WIDTH)
    geo.close()


def test_geospatial_interactive_georeferencer_reference_image_no_crs(test_data, tmpdir):
    """Test for georeferencer with no CRS on reference image"""
    ref_path = str(tmpdir.join("ref.tif"))
    shutil.copy(test_data.small_geotif_no_crs, ref_path)
    img_dir = tmpdir.mkdir("img_dir")
    shutil.copy(test_data.small_geotif_no_crs, str(img_dir.join("target.tif")))

    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="reference_image", reference_image=ref_path,
                                   transform_type="affine", show=False)
    geo._points_layer.data = np.array([[3.0, 3.0], [3.0, 20.0], [16.0, 12.0]])
    geo._on_next()
    geo._points_layer.data = np.array([[4.0, 4.0], [4.0, 18.0], [14.0, 9.0]])
    geo._on_next()
    assert geo.finished
    with pytest.raises(RuntimeError):
        geo.georeference()
    geo.close()


def test_geospatial_interactive_georeferencer_reference_points_not_set(test_data, tmpdir):
    """Test for georeferencer calling georeference with no reference points collected"""
    ref_path = str(tmpdir.join("ref.tif"))
    shutil.copy(test_data.small_geotif, ref_path)
    img_dir = tmpdir.mkdir("img_dir")
    shutil.copy(test_data.small_geotif_no_crs, str(img_dir.join("target.tif")))

    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="reference_image", reference_image=ref_path,
                                   transform_type="affine", show=False)
    # Bypass the normal click flow entirely - gcps has an entry but reference_points was
    # never set, which shouldn't be reachable through the public API but is worth guarding.
    geo.gcps = {"fake_path": [(0, 0), (1, 0), (0, 1)]}
    with pytest.raises(RuntimeError):
        geo.georeference()
    geo.close()


def test_geospatial_interactive_georeferencer_no_points_collected(test_data, tmpdir):
    """Test for georeferencer calling georeference with no points collected"""
    img_dir = tmpdir.mkdir("img_dir")
    shutil.copy(test_data.small_geotif, str(img_dir.join("img.tif")))
    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="known_coordinates",
                                   known_coords=[(500000.0, 4000000.0), (500100.0, 4000000.0), (500050.0, 4000090.0)],
                                   transform_type="affine", show=False)
    with pytest.raises(RuntimeError):
        geo.georeference()
    geo.close()


def test_geospatial_interactive_georeferencer_update_status_label_fallback(test_data, tmpdir):
    """Test for georeferencer's updating of status label"""
    ref_path = str(tmpdir.join("ref.tif"))
    shutil.copy(test_data.small_geotif, ref_path)
    img_dir = tmpdir.mkdir("img_dir")
    shutil.copy(test_data.small_geotif_no_crs, str(img_dir.join("target.tif")))

    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
                                   mode="reference_image", reference_image=ref_path,
                                   transform_type="affine", show=False)
    geo.current_index = 1
    geo._update_status_label()
    assert "Click at least" in geo._status_label.value
    geo.close()


#def test_geospatial_interactive_georeferencer_close(test_data, tmpdir):
#    """Test for plantcv-geospatial."""
#    img_dir = tmpdir.mkdir("img_dir")
#    shutil.copy(test_data.small_geotif, str(img_dir.join("img.tif")))
#    geo = InteractiveGeoreferencer(img_dir=str(img_dir), output_dir=str(tmpdir.join("out")),
#                                   mode="known_coordinates",
#                                   known_coords=[(500000.0, 4000000.0), (500100.0, 4000000.0), (500050.0, 4000090.0)],
#                                   transform_type="affine", show=False)
#    geo.close()


@pytest.mark.parametrize("transform_type", ["affine", "polynomial2", "tps", "projective"])
def test_geospatial_fit_point_transform(transform_type):
    """Test for georeferencing with different transform types"""
    src = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0), (10.0, 10.0), (5.0, 2.0), (2.0, 8.0)]
    dst = [(1.0, 1.0), (11.0, 1.5), (0.5, 11.0), (11.5, 12.0), (6.0, 3.0), (3.0, 9.5)]
    tform = th._fit_point_transform(transform_type, src, dst)
    result = tform(np.array(src))
    assert result.shape == (len(src), 2)


def test_geospatial_fit_point_transform_bad_type():
    """Test for georeferencing with bad transform type"""
    with pytest.raises(RuntimeError):
        th._fit_point_transform("bogus", [(0, 0), (1, 0), (0, 1)], [(0, 0), (1, 0), (0, 1)])


def test_geospatial_fit_point_transform_failed_estimation():
    """Test for georeferencing with a failure to fit due to identical source and dest points"""
    identical = [(5.0, 5.0), (5.0, 5.0), (5.0, 5.0)]
    with pytest.raises(RuntimeError):
        th._fit_point_transform("affine", identical, identical)


def test_geospatial_estimate_pixel_size_degenerate():
    """Test for estimate pixel size falling back to 1 when collinear"""
    collinear = [(0.0, 0.0), (5.0, 0.0), (10.0, 0.0)]
    assert th.estimate_pixel_size(collinear, collinear) == 1.0


def test_geospatial_build_output_grid_too_large():
    """Test for georeferencer when transform fit makes output image too big"""
    src = [(10.0, 10.0), (90.0, 10.0), (10.0, 110.0), (90.0, 110.0), (50.0, 10.0), (50.0, 110.0)]
    dst = [(500000.0 + 3 * x, 4000000.0 + 3 * (120 - y)) for x, y in src]
    with pytest.raises(RuntimeError):
        th.build_output_grid((120, 100, 3), src, dst, "polynomial2", 3.0)


def test_geospatial_build_output_grid_non_finite():
    """Test for georeferencer with a non-finite grid"""
    src = [(float(i * 5), 50.0 + (0.001 if i % 2 else -0.001)) for i in range(10)]
    dst = [(500000.0 + i * 5000.0, 4000000.0) for i in range(10)]
    with pytest.warns(RuntimeWarning), pytest.raises(RuntimeError):
        th.build_output_grid((10**120, 10**120, 3), src, dst, "polynomial3", 1.0)


def test_geospatial_warp_to_grid_float_dtype():
    """Test for georeferencing on non-integer data types"""
    image = (np.random.rand(20, 20, 3) * 100).astype(np.float32)
    src = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0)]
    dst = [(1.0, 1.0), (11.0, 1.0), (1.0, 11.0)]
    warped = th.warp_to_grid(image, (20, 20), dst, src, "affine", 1, None)
    assert warped.dtype == np.float32


@pytest.mark.parametrize("shape", [(20, 20), (20, 20, 1)])
def test_geospatial_make_display_array_grayscale(shape):
    """Test for georeferencer with single band image"""
    array = np.random.rand(*shape) * 100
    display = th.make_display_array(array)
    assert display.shape == shape[:2]
    assert display.dtype == np.uint8


@pytest.mark.parametrize("band,expected_value", [
    (np.full((10, 10), np.nan), 0),
    (np.full((10, 10), 5.0), 128),
])
def test_geospatial_stretch_to_uint8_edge_cases(band, expected_value):
    """Test for georeferencer avoiding divide by zero"""
    result = th._stretch_to_uint8(band)
    assert np.all(result == expected_value)
