from time import sleep

from hexapod_remote.serial import Serial


def main():
    print("starting...")

    serial = Serial()
    serial.wait_for_ping()

    print("ready")

    sleep(0.1)

    serial.send_command("DISABLE_SERVOS")

    for i in range(6):
        serial.send_command(f"SET_LEG_ANGLES {i} 0 90 175")

    serial.send_command("ENABLE_SERVOS")


if __name__ == "__main__":
    main()
