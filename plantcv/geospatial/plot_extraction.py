import math
import fiona
from shapely.geometry import mapping, Polygon, LineString


def create_rectangle_from_points(shapefile_path):
    with fiona.open(shapefile_path, 'r') as shapefile:
        points = [shape['geometry']['coordinates'] for shape in shapefile]
    
    rectangle = Polygon(points)
    return rectangle


def calculate_line_length_in_meters(line):
    total_length = 0
    
    for i in range(len(line.coords)-1):
        x1, y1 = line.coords[i]
        x2, y2 = line.coords[i+1]
        segment_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        total_length += segment_length
    return total_length


def get_field_edges(rectangle):
    coords = list(rectangle.exterior.coords)
    edge1 = LineString([coords[0], coords[1]])
    edge2 = LineString([coords[0], coords[3]])
    return edge1, edge2


def create_grid(rectangle, edge1, edge2, ranges, columns, row_length_along_column, vertical_gap):
    edge1_length = calculate_line_length_in_meters(edge1)
    edge2_length = calculate_line_length_in_meters(edge2)
    horizontal_threshold = edge1_length/columns
    vertical_threshold = row_length_along_column
    divisions_along_edge1 = round(edge1_length / horizontal_threshold)
    divisions_along_edge2 = round((edge2_length - vertical_gap) / (vertical_threshold + vertical_gap)) + 1
    edge1_start = edge1.coords[0]
    edge2_start = edge2.coords[0]

    edge1_dir = ((edge1.coords[1][0] - edge1_start[0]) / edge1.length,
                 (edge1.coords[1][1] - edge1_start[1]) / edge1.length)
    edge2_dir = ((edge2.coords[1][0] - edge2_start[0]) / edge2.length,
                 (edge2.coords[1][1] - edge2_start[1]) / edge2.length)

    grid_cells = []

    for column_number in range(divisions_along_edge1):
        for row_number in range(divisions_along_edge2):
            start_x = edge1_start[0] + column_number * horizontal_threshold * edge1_dir[0] + row_number * (vertical_threshold + vertical_gap) * edge2_dir[0]
            start_y = edge1_start[1] + column_number * horizontal_threshold * edge1_dir[1] + row_number * (vertical_threshold + vertical_gap) * edge2_dir[1]
            bottom_left = (start_x, start_y)
            bottom_right = (bottom_left[0] + horizontal_threshold * edge1_dir[0],
                            bottom_left[1] + horizontal_threshold * edge1_dir[1])
            top_left = (bottom_left[0] + vertical_threshold * edge2_dir[0],
                        bottom_left[1] + vertical_threshold * edge2_dir[1])
            top_right = (bottom_right[0] + vertical_threshold * edge2_dir[0],
                         bottom_right[1] + vertical_threshold * edge2_dir[1])

            cell = Polygon([bottom_left, bottom_right, top_right, top_left, bottom_left])
            if cell.intersects(rectangle):
                grid_cells.append({"polygon": cell, "row": row_number + 1, "column": column_number + 1})

    return grid_cells


def write_shapefile(number_of_ranges, number_of_columns, row_length_along_column, output_shapefile_path, input_shapefile_path, vertical_gap):
    rectangle = create_rectangle_from_points(input_shapefile_path)
    edge1, edge2 = get_field_edges(rectangle)
    grid_cells = create_grid(rectangle, edge1, edge2, number_of_ranges, number_of_columns, row_length_along_column, vertical_gap)

    with fiona.open(input_shapefile_path, 'r') as input_shapefile:
        driver = input_shapefile.driver
        crs = input_shapefile.crs
        schema = {'geometry': 'Polygon', 'properties': {'id': 'int', 'row': 'int', 'column': 'int', 'label': 'str'}}

    with fiona.open(output_shapefile_path, 'w', driver=driver, crs=crs, schema=schema) as output_shapefile:
        for idx, cell in enumerate(grid_cells):
            label = f"({cell['row']},{cell['column']})"
            output_shapefile.write({
                'geometry': mapping(cell["polygon"]),
                'properties': {'id': idx, 'row': cell["row"], 'column': cell["column"], 'label': label},
            })
