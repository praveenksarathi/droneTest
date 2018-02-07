from server.communication import udp
from server.communication import common as com

import settings


class Message:
    def __init__(self):
        self.udp = udp.UdpServer()
        self.drone_ip = '0.0.0.0'
        self.last_frame_part = b""

    def handle_init(self):
        is_correct_init_msg = False
        while not is_correct_init_msg:
            init_msg, drone_ip, _ = self.udp.recv_data()

            if drone_ip == '0.0.0.0':
                continue

            if com.is_init_msg_correct(init_msg):
                is_correct_init_msg = True
                self.drone_ip = drone_ip


    def get_frame(self):
        """
        :return: frame: img data, <ndarray> bytestring format
                 status: status info, <int> representing status:
                         {1: ok
                          2: non correct frame size
                          3: non correct data part
                          4: timeout
                         }
        """

        frame = b""
        status = None

        while True:
            frame_part, _, status = self.udp.recv_data()

            if frame_part[44:] == b"EoF":
                break

            if status == 4:
                return frame, status

            if not com.is_data_part_correct(frame_part, self.last_frame_part):
                status = 3
                break

            self.last_frame_part = frame_part
            frame = frame + frame_part[44:]

        if status is None:
            if com.is_frame_size_correct(frame):
                status = 1
            else:
                status = 2

        return frame, status

    def return_info_to_drone(self, data):
        msg = settings.SERVER_MSG_HEADER + data
        self.udp.send_data(msg, self.drone_ip)
