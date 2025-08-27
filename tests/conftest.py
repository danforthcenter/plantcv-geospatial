import os
import pytest
import matplotlib

# Disable plotting
matplotlib.use("Template")

class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # Flat image directory
        self.snapshot_dir = os.path.join(self.datadir, "snapshot_dir")
        # multispectral image
        self.cropped_tif = os.path.join(self.datadir, "615.tif")
        # multispectral pickled
        self.multi_pickled = os.path.join(self.datadir, "multi_img.spectral")
        # empty image
        self.empty_tif = os.path.join(self.datadir, "cropped_empty.tif")
        # rgb image
        self.rgb_tif = os.path.join(self.datadir, "rgb.tif")
        # rgb uint16 image
        self.rgb_uint16_tif = os.path.join(self.datadir, "rgb_uint16.tif")
        # rgb pickled
        self.rgb_pickled = os.path.join(self.datadir, "rgb_img.spectral")
        # multiPoints shapefilex
        self.pts_geojson = os.path.join(self.datadir, "test_pts.geojson")
        # points shapefilex
        self.single_pts_geojson = os.path.join(self.datadir, "single_test_pts.geojson")
        # polygon shapefile
        self.square_crop = os.path.join(self.datadir, "square_crop.geojson")
        # polygon shapefile with "ID" in properties
        self.geojson_with_id = os.path.join(self.datadir, "square_crop_with_id.geojson")
        # polygon shapefile with "ID" in properties
        self.geojson_with_fid = os.path.join(self.datadir, "square_crop_with_fid.geojson")
        # points shapefile
        self.point_crop = os.path.join(self.datadir, "point_crop.geojson")
        # multi polygon shapefile
        self.multipolygon = os.path.join(self.datadir, "multipolygon_fortests.geojson")
        # epsg4326 points shapefile
        self.epsg4326_geojson = os.path.join(self.datadir, "epsg4326points.geojson")
        # plot bounds shapefile
        self.plot_bounds = os.path.join(self.datadir, "docs_four_points.geojson")
        # plot points shapefile
        self.plot_points = os.path.join(self.datadir, "plot_points.geojson")
        # read netcdf example file and cropping shapefile
        self.test_netcdf = os.path.join(self.datadir, "subset_test.nc")
        self.netcdf_testcrop = os.path.join(self.datadir, "netcdf_test.geojson")

@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV-geospatial package."""
    return TestData()
