import math


def distance_1d(dron_center):
    return (320 - dron_center[0], 240 - dron_center[1])


def distance_2d(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def find_two_vertical_extreme(x_cords, y_cords, kind):
    if kind == 'top':
        first_extreme_index = y_cords.index(min(y_cords))
        first_extreme = (x_cords[first_extreme_index],
                         y_cords[first_extreme_index])
        del y_cords[first_extreme_index]
        del x_cords[first_extreme_index]
        second_extreme_index = y_cords.index(min(y_cords))
        second_extreme = (x_cords[second_extreme_index],
                          y_cords[second_extreme_index])
        return first_extreme, second_extreme

    elif kind == "bottom":
        first_extreme_index = y_cords.index(max(y_cords))
        first_extreme = (x_cords[first_extreme_index],
                         y_cords[first_extreme_index])
        del y_cords[first_extreme_index]
        del x_cords[first_extreme_index]
        second_extreme_index = y_cords.index(max(y_cords))
        second_extreme = (x_cords[second_extreme_index],
                          y_cords[second_extreme_index])
        return first_extreme, second_extreme


def find_horizontal_extreme(points):
    x_cords = (points[0][0], points[1][0])
    most_right_index = x_cords.index(max(x_cords))
    return points[most_right_index]
