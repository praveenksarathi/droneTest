import socket
import time
import signal

import settings


class UdpServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(settings.UDP_SERVER_ADDRESS)
        signal.signal(signal.SIGALRM, self._timeout_handler)

    def _timeout_handler(self, signum, frame):
        raise Exception("Timeout error when waiting for data")
        #raise TimeoutError("Timeout error when waiting for data")

    def send_data(self, data, client_address):
        self.server_socket.sendto(data, client_address)
        time.sleep(0.01)

    def recv_data(self):
        signal.setitimer(signal.ITIMER_REAL, settings.MAX_RECV_TIME)

        try:
            data, ip = self.server_socket.recvfrom(settings.UDP_DATA_PART_SIZE)
            status = None
        except Exception as toe:
            data = b""
            ip = '0.0.0.0'
            status = 4
            print(toe)

        signal.setitimer(signal.ITIMER_REAL, 0)

        return data, ip, status
