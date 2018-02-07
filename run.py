from server.communication import message
from server.processing_algorithm import img_processing

import settings

if __name__ == "__main__":
    listener_var = message.Message()
    listener_var.handle_init()

    while True:
        print("Received frame")

        frame, status = listener_var.get_frame()

        result_status = bytes(str(status))
        if status == 1:
            offset = result_status + img_processing.img(frame)
        else:
            offset = result_status + settings.FAILED_RESULT

        eot_msg = result_status + settings.EOT_RESULT

        listener_var.return_info_to_drone(offset)
        listener_var.return_info_to_drone(eot_msg)
