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
        # rgb image
        self.rgb_tif = os.path.join(self.datadir, "rgb.tif")
        # points shapefilex
        self.pts_geojson = os.path.join(self.datadir, "monday_test_points.shp")

@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV-geospatial package."""
    return TestData()
