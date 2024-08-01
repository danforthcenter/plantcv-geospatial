"""Tests for geospatial.readd_geotif."""

import pytest
from plantcv.geospatial import transform_points


def test_geospatial_transform_points(test_data):
    """Test for plantcv-geospatial."""
    # read in small 5-band tif image
    coords = transform_points(img=test_data.cropped_tif, geojson=test_data.pts_geojson)
