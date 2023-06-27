#!/usr/bin/env python3

import logging
from datetime import datetime

import serial
from decouple import config

logger = logging.getLogger(__name__)

SERIAL_PORT = config("SERIAL_PORT", default="/dev/ttyUSB0")
BAUD_RATE = config("BAUD_RATE", default=115200)
SERIAL_TIMEOUT = config("SERIAL_TIMEOUT", default=0.01, cast=int)


if __name__ == '__main__':
    serial_port = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)

    while True:
        command = input("> ")
        t1 = datetime.now()

        serial_port.write(command.encode())

        t2 = datetime.now()
        logger.debug(f"Time to send: {t2 - t1}")

        while True:
            t2 = datetime.now()
            line = serial_port.readline()
            t3 = datetime.now()
            logger.debug(f"Time to receive: {t3 - t2}")

            try:
                line = line.decode()
                line = line.strip()

                if not line:
                    break

                print(line)
            except UnicodeDecodeError:
                pass
