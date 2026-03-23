class Field_layout:
    """PlantCV-Geospatial field layout metadata class."""

    def __init__(self, num_ranges=None, num_columns=None, range_length=None,
                 row_length=None, num_rows=1, range_spacing=0, column_spacing=0):
        """Initialize parameters.

        Parameters
        ----------
        num_ranges : int
            Number of ranges in the field layout.
        num_columns : int
            Number of columns in the field layout.
        range_length : float
            Length of each range in units that should match input shapefiles.
        row_length : float
            Length of each row in a plot.
        num_rows: int, optional
            Number of rows in a plot. Defaults to 1.
        range_spacing : float, optional
            Length of alleys between ranges. Defaults to 0.
        column_spacing : float, optional
            Lenght of alleys between columns. Defaults to 0.
        """
        self.num_ranges = num_ranges
        self.num_columns = num_columns
        self.range_length = range_length
        self.row_length = row_length
        self.num_rows = num_rows
        self.range_spacing = range_spacing
        self.column_spacing = column_spacing


# Initialize an instance of Field_layout class with default values
# Field_layout is available when PlantCV-Geospatial is imported
field_layout = Field_layout()
