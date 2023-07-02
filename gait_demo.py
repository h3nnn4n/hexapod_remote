import argparse
from time import sleep

from hexapod_remote.serial import Serial


def connect() -> Serial:
    print("starting...")

    serial = Serial()
    serial.wait_for_ping()

    print("ready")

    serial.send_command("ENABLE_SERVOS")

    return serial


def set_starting_position(serial: Serial) -> None:
    """
    Set all legs to the "rest" position, one by one.

    To be safer, the robot should already be physically close to the target
    positions.
    """
    serial.disable_auto_send()
    serial.set_leg_mode("INSTANTANEOUS")
    for i in range(6):
        serial.set_leg_angles(i, 0, 90, 162.5)
    serial.send_commands()


def standup(serial: Serial, height: float = 100) -> None:
    serial.disable_auto_send()
    serial.set_legs_speed(50.0)
    serial.set_leg_mode("CONSTANT_SPEED")

    distance_from_body = 95

    for leg_index in range(6):
        serial.set_leg_position(leg_index, 0, distance_from_body, -height)

    serial.send_commands()


def set_height(serial: Serial, height: float = 100) -> None:
    serial.disable_auto_send()

    for leg_index in range(6):
        serial.set_leg_position(leg_index, 0, 95, -height)

    serial.send_commands()


def calibration_position(serial: Serial) -> None:
    serial.disable_auto_send()

    angle_coxa = 0
    angle_femur = 0
    angle_tibia = 0

    for leg_index in range(6):
        serial.set_leg_angles(leg_index, angle_coxa, angle_femur, angle_tibia)

    serial.send_commands()


def walk_forward(serial: Serial, stride_length: float = 50, distance_from_body: float = 95) -> None:
    leg_group_1 = [0, 2, 4]
    leg_group_2 = [1, 3, 5]

    ground_height = -120
    feet_up_height = -80

    walk_speed = 150
    sleep_time = 0.75
    sleep_time2 = 0.5

    serial.disable_auto_send()
    serial.set_legs_speed(walk_speed)
    serial.set_leg_mode("CONSTANT_SPEED")
    serial.send_commands()

    while True:
        # Part 1
        for leg in leg_group_1:
            serial.set_leg_position(leg, -stride_length, distance_from_body, feet_up_height)

        for leg in leg_group_2:
            serial.set_leg_position(leg, stride_length, distance_from_body, ground_height)
        serial.send_commands()
        sleep(sleep_time)
        print()

        for leg in leg_group_1:
            serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
        serial.send_commands()
        sleep(sleep_time2)
        print()

        # Part 2
        for leg in leg_group_2:
            serial.set_leg_position(leg, stride_length, distance_from_body, feet_up_height)

        for leg in leg_group_1:
            serial.set_leg_position(leg, stride_length, distance_from_body, ground_height)
        serial.send_commands()
        sleep(sleep_time)
        print()

        for leg in leg_group_2:
            serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
        serial.send_commands()
        sleep(sleep_time2)
        print()


def translate_body_up_and_down(serial: Serial) -> None:
    sleep_time = 3.0
    low_height = -250
    high_height = -75
    distance_from_body = 95

    serial.disable_auto_send()
    serial.set_legs_speed(50.0)
    serial.set_leg_mode("CONSTANT_SPEED")
    serial.send_commands()

    while True:
        for leg in range(6):
            serial.set_leg_position(leg, 0, distance_from_body, low_height)
        serial.send_commands()
        sleep(sleep_time)
        print()

        for leg in range(6):
            serial.set_leg_position(leg, 0, distance_from_body, high_height)
        serial.send_commands()
        sleep(sleep_time)
        print()


def walk_in_place(serial: Serial) -> None:
    leg_group_1 = [0, 2, 4]
    leg_group_2 = [1, 3, 5]

    ground_height = -120
    feet_up_height = -75
    distance_from_body = 95
    stride_length = 0

    sleep_time = 0.75
    walk_speed = 100

    serial.disable_auto_send()
    serial.set_legs_speed(walk_speed)
    serial.set_leg_mode("CONSTANT_SPEED")
    serial.send_commands()

    while True:
        # Part 1
        for leg in leg_group_1:
            serial.set_leg_position(leg, -stride_length, distance_from_body, feet_up_height)
        serial.send_commands()
        sleep(sleep_time)
        print()

        for leg in leg_group_1:
            serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
        serial.send_commands()
        sleep(sleep_time)
        print()

        # Part 2
        for leg in leg_group_2:
            serial.set_leg_position(leg, stride_length, distance_from_body, feet_up_height)
        serial.send_commands()
        sleep(sleep_time)
        print()

        for leg in leg_group_2:
            serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
        serial.send_commands()
        sleep(sleep_time)
        print()


def angle_offset_test(serial: Serial) -> None:
    sleep_time = 1.0
    height = -110

    serial.set_legs_speed(50.0)
    serial.set_leg_mode("CONSTANT_SPEED")

    serial.disable_auto_send()

    for _ in range(10):
        for i in range(6):
            serial.set_leg_position(i, 0, 80, height)
        serial.send_commands()

        print()
        sleep(sleep_time)

        for i in range(6):
            serial.set_leg_position(i, 0, 120, height)
        serial.send_commands()

        print()
        sleep(sleep_time)


def main(action: str) -> None:
    serial = connect()

    match (action):
        case "starting_position":
            set_starting_position(serial)

        case "calibration":
            calibration_position(serial)

        case "walk_in_place":
            walk_in_place(serial)

        case "walk_forward":
            walk_forward(serial)

        case "walk_backward":
            walk_forward(serial, stride_length=-50)

        case "up_and_down":
            translate_body_up_and_down(serial)

        case "standup":
            standup(serial, 120)

        case "standup_tall":
            standup(serial, 225)

        case "angle_offset_test":
            angle_offset_test(serial)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control the hexapod robot")
    parser.add_argument("action", type=str, help="Action to perform")
    args = parser.parse_args()

    main(action=args.action)
