from time import sleep

import serial

from hexapod_remote import config


class Serial:
    def __init__(self):
        self._port = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=config.SERIAL_TIMEOUT)

    def send_command(self, command: str) -> None:
        print(command)
        self.write(command)
        self.wait_for_ok()

    def write(self, data: str) -> None:
        if not data.endswith("\n"):
            data += "\n"

        self._port.write(data.encode())

    def readline(self) -> str:
        return self._port.readline().decode().strip()

    def wait_for_ok(self) -> None:
        while True:
            line = self.readline()

            if line == "OK":
                break

            sleep(0.1)

    def wait_for_ping(self) -> None:
        while True:
            sleep(0.1)

            self.write("PING")

            sleep(0.1)

            line = self.readline()
            if line == "PONG":
                break
