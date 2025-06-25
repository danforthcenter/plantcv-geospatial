"""Tests for geospatial.read_netcdf."""

import os
from plantcv.geospatial import read_netcdf


def test_geospatial_read_netcdf(test_data, tmpdir):
    """Test for plantcv-geospatial."""
    # read in small netcdf file
    cache_dir = tmpdir.mkdir("cache")
    outfile = os.path.join(str(cache_dir), "netcdf_output.tif")
    img = read_netcdf(filename=test_data.test_netcdf, cropto=test_data.netcdf_testcrop, output=outfile) 
    assert img.array_data.shape == (2, 2, 21)