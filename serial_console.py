import logging
from datetime import datetime

from hexapod_remote.serial import Serial


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    serial = Serial()
    serial.wait_for_ping()

    while True:
        command = input("> ")
        t1 = datetime.now()

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

            print(line)
