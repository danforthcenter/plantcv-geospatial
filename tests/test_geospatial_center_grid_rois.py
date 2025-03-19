"""Tests for geospatial.napari_grid and geospatial.napari_polygon_grid"""

import napari
import joblib
import plantcv.geospatial as geo
import numpy as np


def test_geospatial_center_rois_one(test_data):
    """Test for plantcv-geospatial."""
    field = np.array([[64.11229125, 128.74165877],
                      [136.25692447, 203.82241079],
                      [213.85434974, 139.64724287],
                      [140.45137989,  59.95258989]])
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes(field, name="grid_shapes")
    rois = geo.center_grid_rois(img.pseudo_rgb, viewer, radius=10)
    assert len(rois.contours) == 1
    viewer.close()


def test_geospatial_center_rois_multi(test_data):
    """Test for plantcv-geospatial."""
    field = [np.array([[33.91221223, 186.62514357],
                       [71.24286547, 238.63639077],
                       [111.92908304, 196.27239103],
                       [73.34009318, 151.81116358]]), 
             np.array([[98.08738015, 122.86942119],
                       [143.80694423, 174.88066839],
                       [187.00983506, 135.0333419],
                       [143.80694423,  83.44154024]])]
    img = joblib.load(test_data.rgb_pickled)
    viewer = napari.Viewer(show=False)
    viewer.add_image(img.pseudo_rgb)
    viewer.add_shapes(field, name="grid_shapes")
    rois = geo.center_grid_rois(img.pseudo_rgb, viewer, radius=10)
    assert len(rois.contours) == 2
    viewer.close()
