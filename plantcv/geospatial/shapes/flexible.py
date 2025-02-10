# Create rectangular geojsons

from shapely.geometry import Polygon, mapping
from plantcv.geospatial import _helpers
import fiona


def flexible(img, field_corners, plot_geojson_path, out_path, num_rows=8, range_length=3.6576, column_length=0.9144):
    """Create a grid of cells from input shapefiles and save them to a new shapefile.

    Parameters:
    -----------
    img : [spectral_object]
        Spectral_Data object of geotif data, used for plotting
    field_corners : str
        Path to geojson containing four corner points
    plot_geojson_path : str
        Path to geojson containing plot corner points
    out_path : str
        Path where the output grid cells geojson will be saved
    num_rows : int, optional
        Number of rows per plot, default: 8
    range_length : float, optional
        Height of each grid cell (default: 3.6576m )
    column_length : float, optional
        Width of each grid cell (default: 0.9144m )

    Returns:
    --------
    fig
        matplotlib figure displaying the created grid cell polygons
    """
    # Calculate direction vectors based on plot boundaries
    horizontal_dir, vertical_dir, _, crs, driver, schema = _helpers._calc_direction_vectors(
        plot_bounds=field_corners)
    # Read the plot boundaries shapefile
    with fiona.open(plot_geojson_path, 'r') as shapefile:
        plot_corner_points = _helpers._unpack_point_shapefiles(shapefile)

    # Initialize list for storing grid cells
    grid_cells = []

    # Create grid cells for each plot
    for points in plot_corner_points:
        for col_num in range(num_rows):
            anchor_point = points
            p1, p2, p3, p4 = _helpers._calc_plot_corners(
                anchor_point, horizontal_dir, vertical_dir,
                col_num, range_num=0, range_length=range_length,
                column_length=column_length)

            # Create polygon from corners
            cell = Polygon([p1, p2, p4, p3, p1])
            grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(out_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })
    # Debug image of the output shapefile
    fig = _helpers._show_geojson(img, out_path)
    return fig
