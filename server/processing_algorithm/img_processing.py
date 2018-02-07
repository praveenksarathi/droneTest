import server.processing_algorithm.preprocessing as preprocessing
import server.processing_algorithm.marker as marker
import server.processing_algorithm.drone_offsets as drone_offsets
import settings


def img(raw_frame):
    prepared_image = preprocessing.prepare_img(raw_frame)
    contours = preprocessing.find_contours(prepared_image)
    square_marker = marker.find_marker(contours)

    if not square_marker:
        print("square marker not found :(")
        return settings.FAILED_RESULT
    offsets = drone_offsets.get_offsets(square_marker)

    result = str(offsets["offset_x"]) + ":" + \
             str(offsets["offset_y"]) + ":" + \
             str(offsets["offset_z"])
    result = bytearray(result, encoding="utf-8")

    return result
