from time import sleep

from hexapod_remote.serial import Serial


def main():
    print("starting...")

    serial = Serial()
    serial.wait_for_ping()

    print("ready")

    sleep(0.1)

    serial.send_command("ENABLE_SERVOS")

    serial.disable_auto_send()

    while True:
        serial.set_leg_position(4, 0, 140, -120)
        serial.set_leg_position(1, 0, 140, -120)
        serial.send_commands()
        # sleep(0.5)

        serial.set_leg_position(4, -50, 140, -140)
        serial.set_leg_position(1, -50, 140, -140)
        serial.send_commands()
        # sleep(0.5)

        serial.set_leg_position(4, 50, 140, -140)
        serial.set_leg_position(1, 50, 140, -140)
        serial.send_commands()
        # sleep(0.5)


if __name__ == "__main__":
    main()
