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
    sleep(0.5)
    for i in range(6):
        sleep(0.5)
        serial.set_leg_angles(i, 0, 90, 175)


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


def main():
    serial = connect()
    set_starting_position(serial)
    standup(serial, 120)


if __name__ == "__main__":
    main()
