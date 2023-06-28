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
    for i in range(6):
        serial.set_leg_position(i, 0, 100, -100)
    serial.send_commands()

    # serial.enable_auto_send()

    # serial.set_leg_position(2, 50, 100, -140)

    # serial.send_command("READ_LEG_INFO 2")

    return

    legs = [5, 3, 1]
    # legs = [0, 3, 2, 5]
    # legs = [0, 3]

    while True:
        for leg in legs:
            serial.set_leg_position(leg, -30, 100, -120)
        serial.send_commands()
        sleep(0.25)

        for leg in legs:
            serial.set_leg_position(leg, 0, 100, -120)
        serial.send_commands()
        sleep(0.25)

        for leg in legs:
            serial.set_leg_position(leg, 30, 100, -120)
        serial.send_commands()
        sleep(0.25)

        for leg in legs:
            serial.set_leg_position(leg, 0, 100, -120)
        serial.send_commands()
        sleep(0.25)


if __name__ == "__main__":
    main()
