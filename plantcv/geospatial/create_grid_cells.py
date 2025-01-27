#
from shapely.geometry import LineString, Polygon, mapping
import fiona



def create_grid_cells(four_points_path, plot_shapefile_path, output_path, horizontal_cells=8, vertical_length=3.6576, horizontal_length=0.9144):
    """Create a grid of cells from input shapefiles and save them to a new shapefile.

    Parameters:
    -----------
    four_points_path : str
        Path to shapefile containing four corner points
    plot_shapefile_path : str
        Path to shapefile containing plot boundaries
    output_path : str
        Path where the output grid cells shapefile will be saved
    horizontal_cells : int, optional
        Number of cells to divide the horizontal edge into (default: 8)
    vertical_length : float, optional
        Height of each grid cell (default: 3.6576m )
    horizontal_length : float, optional
        Width of each grid cell (default: 0.9144m )

    Returns:
    --------
    list
        List of dictionaries containing the created grid cell polygons
    """

    # Read the four corner points shapefile
    with fiona.open(four_points_path, 'r') as shapefile:
        coordinates = [shape['geometry']['coordinates'] for shape in shapefile]
        crs = shapefile.crs
        driver = shapefile.driver
        schema = {
            'geometry': 'Polygon',
            'properties': {} 
        }

    # Read the plot boundaries shapefile
    with fiona.open(plot_shapefile_path, 'r') as shapefile:
        plot_corner_points = [shape['geometry']['coordinates'] for shape in shapefile]

    # Create LineString objects for edges
    # NOTE: order will depend on order that 4 corners are clicked in
    edge_1 = LineString([coordinates[3][0], coordinates[0][0]])  # vertical edge
    edge_2 = LineString([coordinates[0][0], coordinates[1][0]])  # horizontal edge

    # Calculate direction vectors
    edge_1_dir = ((edge_1.coords[1][0] - edge_1.coords[0][0]) / edge_1.length,
                  (edge_1.coords[1][1] - edge_1.coords[0][1]) / edge_1.length)
    edge_2_dir = ((edge_2.coords[1][0] - edge_2.coords[0][0]) / edge_2.length,
                  (edge_2.coords[1][1] - edge_2.coords[0][1]) / edge_2.length)

    # Cell width
    horizontal_threshold = horizontal_length

    # Initialize list for storing grid cells
    grid_cells = []

    # Create grid cells for each plot
    for points in plot_corner_points:
        for column_number in range(horizontal_cells):
            # Calculate corners of each grid cell
            bottom_left = (points[0] + column_number * horizontal_threshold * edge_2_dir[0],
                           points[1] + column_number * horizontal_threshold * edge_2_dir[1])

            bottom_right = (bottom_left[0] + horizontal_threshold * edge_2_dir[0],
                            bottom_left[1] + horizontal_threshold * edge_2_dir[1])

            top_left = (bottom_left[0] + vertical_length * edge_1_dir[0],
                        bottom_left[1] + vertical_length * edge_1_dir[1])

            top_right = (bottom_right[0] + vertical_length * edge_1_dir[0],
                         bottom_right[1] + vertical_length * edge_1_dir[1])

            # Create polygon from corners
            cell = Polygon([bottom_left, bottom_right, top_right, top_left, bottom_left])
            grid_cells.append({"polygon": cell})

    # Save grid cells to output shapefile
    with fiona.open(output_path, 'w', driver=driver, crs=crs, schema=schema) as shapefile:
        for cell in grid_cells:
            shapefile.write({
                'geometry': mapping(cell["polygon"])
            })

    return grid_cells
