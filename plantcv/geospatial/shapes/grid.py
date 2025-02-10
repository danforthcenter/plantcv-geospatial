# Create rectangular geojsons

from shapely.geometry import Polygon, mapping
from plantcv.geospatial import _helpers
import fiona


def grid(img, field_corners, out_path, num_ranges, num_columns, num_rows=4, range_length=3.6576, column_length=0.9144, range_spacing=0, column_spacing=0):
    """Create a grid of cells from input shapefiles and save them to a new shapefile.

    Parameters:
    -----------
    img : [spectral_object]
        Spectral_Data object of geotif data, used for plotting
    field_corners : str
        Path to geojson containing four corner points
    out_path : str
        Path where the output grid cells geojson will be saved
    range_spacing : float
        Size of alley spaces beteen ranges (default: 0)
    column_spacing : float
        Size of alley spaces beteen columns (default: 0)
    num_ranges : int
        Number of ranges (vertical cell rows)
    num_columns : int
        Number of columns (horizontal cell columns)
    num_rows : int, optional
        Number of cells to divide the horizontal edge into (default: 4)
    range_length : float, optional
        Height of each grid cell (default: 3.6576)
    column_length : float, optional
        Width of each grid cell (default: 0.9144)

    Returns:
    --------
    fig
        matplotlib figure displaying the created grid cell polygons
    """
    # Calculate direction vectors based on plot boundaries
    horizontal_dir, vertical_dir, anchor_point, crs, driver, schema = _helpers._calc_direction_vectors(
        plot_bounds=field_corners)

    # Initialize list for storing grid cells
    grid_cells = []

    # Create grid cells for each plot
    for range_number in range(num_ranges):
        for column_number in range(num_columns):
            p1, p2, p3, p4 = _helpers._calc_plot_corners(anchor_point, horizontal_dir, vertical_dir,
                                                         col_num=column_number, range_num=range_number,
                                                         range_length=range_length, column_length=column_length,
                                                         range_spacing=range_spacing, column_spacing=column_spacing)

            # Create polygon from corners
            cell = Polygon([p1, p2, p4, p3, p1])
            subcells = _helpers._split_subplots(polygon=cell, num_divisions=num_rows)
            for cell in subcells:
                grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(out_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })
    fig = _helpers._show_geojson(img, out_path)
    return fig
