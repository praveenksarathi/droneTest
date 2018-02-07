from server.communication import error

import settings


def is_init_msg_correct(init_msg):
    if is_auth_msg_correct(init_msg) and init_msg[44:] == b"init":
        return True
    else:
        error.non_correct_init_msg()
        return False


def is_auth_msg_correct(auth_msg):
    _, _, drone_id, drone_auth_key = split_header_msg(auth_msg)

    if drone_id != settings.DRONE_ID:
        error.non_correct_auth_data()
        return False

    if drone_auth_key != settings.DRONE_AUTH_KEY:
        error.non_correct_auth_data()
        return False

    return True


def is_data_part_correct(current_data_part, last_data_part):
    if not is_auth_msg_correct(current_data_part):
        print("Failed auth")
        return False

    if not is_msg_order_correct(current_data_part, last_data_part):
        print("Failed order")
        return False

    if current_data_part[44:] == b"EoF":
        return True

    return True


def is_msg_order_correct(current_msg, last_msg):
    c_part_number = current_msg[:4]
    l_part_number = last_msg[:4]

    if c_part_number == b"0001":
        return True

    if int(c_part_number.decode()) == int(l_part_number.decode()) + 1:
        return True
    else:
        error.non_correct_data_order()
        return False


def split_header_msg(header_msg):
    part_number = int(header_msg[:4].decode())
    part_count = int(header_msg[4:8].decode())
    dron_id = header_msg[8:12]
    dron_auth_key = header_msg[12:44]

    return part_number, part_count, dron_id, dron_auth_key


def is_frame_size_correct(frame):
    frame_size = len(frame)
    if frame_size == settings.FRAME_SIZE:
        return True
    else:
        return False
