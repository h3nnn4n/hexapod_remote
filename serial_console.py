import logging
from datetime import datetime
from time import sleep

from hexapod_remote.serial import Serial


logger = logging.getLogger(__name__)


def proccess_data(data: str) -> list[str]:
    lines = data.splitlines()
    lines = [line.strip() for line in lines]
    lines = [line.partition("#")[0] for line in lines]
    lines = [line for line in lines if line]
    lines = [line + "\n" for line in lines]
    return lines


if __name__ == "__main__":
    serial = Serial()
    serial.wait_for_ping()
    print("ready")

    while True:
        try:
            commands = input()
        except EOFError:
            break

        for command in proccess_data(commands):
            t1 = datetime.now()

            if command.startswith("SLEEP "):
                _, _, sleep_time = command.partition(" ")
                print(command)
                sleep(float(sleep_time))
                continue

            serial.write(command)

            t2 = datetime.now()
            logger.debug(f"Time to send: {t2 - t1}")

            while True:
                t2 = datetime.now()
                line = serial.readline()
                t3 = datetime.now()
                logger.debug(f"Time to receive: {t3 - t2}")

                if not line:
                    break

                print(f"{line}")
