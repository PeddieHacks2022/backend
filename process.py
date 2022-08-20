
def bounding_box(points):

    max_x = float('-inf')
    max_y = float('-inf')
    min_x = float('inf')
    min_y = float('inf')

    for point in points:
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])
        min_x = min(min_x, point[0])
        min_x = min(min_y, point[1])

    return (min_x, min_y)

def shift_coords(x_shift, y_shift, points):
    return [(point[0]-x_shift, point[1]-y_shift) for point in points]
