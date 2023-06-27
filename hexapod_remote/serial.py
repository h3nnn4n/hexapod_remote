import serial
from time import sleep

from hexapod_remote import config


class Serial:
    def __init__(self):
        self._port = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=config.SERIAL_TIMEOUT)

    def write(self, data: str):
        self._port.write((data).encode())

    def readline(self) -> str:
        return self._port.readline().decode().strip()

    def wait_for_ping(self):
        while True:
            self.write("PING\n")

            line = self.readline()
            if line == "PONG":
                break

            sleep(0.1)
