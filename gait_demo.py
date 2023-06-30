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
    for i in range(6):
        serial.set_leg_angles(i, 0, 90, 175)
    serial.send_commands()


def standup(serial: Serial, height: float = 100, n_steps: int = 15) -> None:
    serial.disable_auto_send()

    starting_height = 80
    step = (height - starting_height) / n_steps

    for i in range(n_steps + 1):
        h = 0.0 - (starting_height + i * step)
        h = round(h, 1)

        for leg_index in range(6):
            serial.set_leg_position(leg_index, 0, 70, h)

        serial.send_commands()


def set_height(serial: Serial, height: float = 100) -> None:
    serial.disable_auto_send()

    for leg_index in range(6):
        serial.set_leg_position(leg_index, 0, 60, -height)

    serial.send_commands()


def main():
    serial = connect()

    serial.set_leg_mode("INSTANTANEOUS")
    set_height(serial, 140)

    serial.enable_auto_send()

    serial.set_legs_speed(5000.0)
    serial.set_leg_mode("CONSTANT_SPEED")

    serial.disable_auto_send()

    serial.set_leg_position(0, 0, 60, -80)
    serial.set_leg_position(2, 0, 60, -80)
    serial.set_leg_position(4, 0, 60, -80)
    serial.send_commands()
    sleep(2.5)
    serial.set_leg_position(0, 0, 60, -140)
    serial.set_leg_position(2, 0, 60, -140)
    serial.set_leg_position(4, 0, 60, -140)
    serial.send_commands()
    sleep(2.5)

    serial.set_leg_position(1, 0, 60, -80)
    serial.set_leg_position(3, 0, 60, -80)
    serial.set_leg_position(5, 0, 60, -80)
    serial.send_commands()
    sleep(2.5)
    serial.set_leg_position(1, 0, 60, -140)
    serial.set_leg_position(3, 0, 60, -140)
    serial.set_leg_position(5, 0, 60, -140)
    serial.send_commands()
    sleep(2.5)

    # for i in range(6):
    # print()
    # serial.set_leg_position(i, 0, 60, -80)
    # sleep(2.5)
    # serial.set_leg_position(i, 0, 60, -140)
    # sleep(2.5)

    # serial.set_leg_mode("INSTANTANEOUS")
    # set_height(serial, 83.5)

    # serial.set_legs_speed(100.0)
    # serial.set_leg_mode("CONSTANT_SPEED")
    # serial.send_commands()

    # set_height(serial, 170)

    # set_height(serial, 70)
    # set_height(serial, 170)
    # while True:
    # set_height(serial, 70)
    # set_height(serial, 170)


if __name__ == "__main__":
    main()
