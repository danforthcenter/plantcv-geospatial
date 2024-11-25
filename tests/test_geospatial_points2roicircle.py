"""Tests for geospatial.points2roi_circle"""

from plantcv.geospatial import read_geotif, points2roi_circle


def test_geospatial_points2roi_circle(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    img = read_geotif(filename=test_data.rgb_tif, bands="B,G,R")
    rois = points2roi_circle(img=img, geojson=test_data.pts_geojson, radius=0.5)
    assert rois.contours[0][:6] == [[119, 170], [119, 172], [119, 175], [118, 177], [118, 179], [117, 181]]
