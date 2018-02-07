import server.processing_algorithm.common as com

import settings


def _marker_height(ray):
    marker_height = com.distance_2d(ray[0], ray[1])
    return marker_height


def _calc_distance_coefficient(ray):
    marker_height = _marker_height(ray)
    distance_coefficient = settings.REAL_MARKER_HEIGHT / marker_height
    return distance_coefficient


def _calc_offset_angle(angle):
    offset_angle = 90.0 - angle
    return offset_angle


def _calc_offset_distance(marker_center, distance_coefficient):
    offset = com.distance_1d(marker_center)

    offset_x = offset[0] * distance_coefficient
    offset_y = offset[1] * distance_coefficient
    return offset_x, offset_y


def get_offsets(marker):
    distance_coefficient = _calc_distance_coefficient(marker["ray"])
    offset_angle = _calc_offset_angle(marker["angle"])
    offset_x, offset_y = _calc_offset_distance(marker["marker_center"],
                                               distance_coefficient)
    offset_z = (settings.REAL_MARKER_HEIGHT * settings.FOCAL_LENGTH) / _marker_height(marker["ray"])

    return {"offset_angle": offset_angle,
            "offset_x": offset_x,
            "offset_y": offset_y,
            "offset_z": offset_z,
            "distance_coefficient": distance_coefficient
            }
