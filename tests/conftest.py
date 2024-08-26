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
        # empty image
        self.empty_tif = os.path.join(self.datadir, "cropped_empty.tif")
        # rgb image
        self.rgb_tif = os.path.join(self.datadir, "rgb.tif")
        # multiPoints shapefilex
        self.pts_geojson = os.path.join(self.datadir, "test_pts.geojson")
        # points shapefilex
        self.single_pts_geojson = os.path.join(self.datadir, "single_test_pts.geojson")
        # polygon shapefile
        self.square_crop = os.path.join(self.datadir, "square_crop.geojson")
        # points shapefile
        self.point_crop = os.path.join(self.datadir, "point_crop.geojson")

@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV-geospatial package."""
    return TestData()
