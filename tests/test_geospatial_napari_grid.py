"""Tests for geospatial.napari_grid and geospatial.napari_polygon_grid"""

import pytest
import joblib
import napari
import plantcv.geospatial as geo
import numpy as np
from plantcv.geospatial.napari_polygon_grid import _lineintersect


def test_geospatial_napari_grid(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes(field, name="field_polygon")
    geo.napari_grid(viewer, numdivs=[1, 2], layername="field_polygon")
    geo.napari_polygon_grid(viewer)
    assert len(viewer.layers["grid_lines1"].data) == 2
    assert len(viewer.layers["grid_shapes"].data) == 2
    assert viewer.layers["grid_lines1"].data[0][1][0] == 140.45139
    assert viewer.layers["grid_shapes"].data[0][1][0] == 136.25692447
    viewer.close()


def test_geospatial_lineintersect():
    """Test for plantcv-geospatial."""
    with pytest.raises(RuntimeError):
        _ = _lineintersect([(0, 0), (0, 1)], [(1, 0), (1, 1)])
