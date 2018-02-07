import cv2
import math

import server.processing_algorithm.common as com


def _find_corners(contour):
    perimeter = cv2.arcLength(contour, True)
    corners = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
    return corners


def _is_square(corners):
    if len(corners) == 4:
        (x, y, width, height) = cv2.boundingRect(corners)
        aspect_ratio = width / float(height)
        if width > 10 or height > 10:
            if 0.90 <= aspect_ratio <= 1.1:
                return True
    return False


def _find_ray(corners):
    x_cords = [corners[x][0][0] for x in range(len(corners))]
    y_cords = [corners[y][0][1] for y in range(len(corners))]

    top_points = com.find_two_vertical_extreme(x_cords, y_cords, "top")
    top_most_right = com.find_horizontal_extreme(top_points)

    bottom_points = com.find_two_vertical_extreme(x_cords, y_cords, "bottom")
    bottom_most_right = com.find_horizontal_extreme(bottom_points)

    return top_most_right, bottom_most_right


def _find_marker_center(contours):
    moments = cv2.moments(contours)
    center_x = int(moments["m10"] / moments["m00"])
    center_y = int(moments["m01"] / moments["m00"])
    marker_center = (center_x, center_y)
    return marker_center


def _calc_angle(ray_top, ray_bottom):
    point_bottom_most_right = (310, ray_bottom[1])
    a = com.distance_2d(ray_top, point_bottom_most_right)
    b = com.distance_2d(ray_top, ray_bottom)
    c = com.distance_2d(ray_bottom, point_bottom_most_right)

    try:
        angle = math.acos(
            (math.pow(b, 2) + math.pow(c, 2) - math.pow(a, 2)) / (2 * b * c))
    except ZeroDivisionError:
        angle = math.acos((math.pow(b, 2) + math.pow(c, 2) - math.pow(
            a, 2)) / (2 * b + 0.00000001 * c + 0.0000001))

    return math.degrees(angle)


def _identify_view_type(corners):
    for points in range(len(corners)):
        if corners[points][0][1] in (0, 1, 2, 3, 477, 478, 479, 480):
            return False
        if corners[points][0][0] in (0, 1, 2, 3, 637, 638, 639, 640):
            return False
    return True


def find_marker(contours):
    for c in contours:
        corners = _find_corners(c)
        is_square = _is_square(corners)
        if not is_square:
            continue
        marker_center = _find_marker_center(c)
        ray_top, ray_bottom = _find_ray(corners)
        angle = _calc_angle(ray_top, ray_bottom)
        status = _identify_view_type(corners)
        return {"status": status,
                "corners": corners,
                "contour": c,
                "ray": (ray_top, ray_bottom),
                "marker_center": marker_center,
                "angle": angle,
                }
    return False
