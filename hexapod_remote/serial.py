from time import sleep

import serial

from hexapod_remote import config


class Serial:
    def __init__(self, auto_send: bool = True):
        self._port = serial.Serial(config.SERIAL_PORT, config.BAUD_RATE, timeout=config.SERIAL_TIMEOUT)
        self._auto_send = auto_send
        self._queue = []

    def disable_auto_send(self) -> None:
        self._auto_send = False

    def enable_auto_send(self) -> None:
        self._auto_send = True

    def set_auto_send(self, auto_send: bool) -> None:
        self._auto_send = auto_send

        if auto_send:
            self.send_commands()

    def send_commands(self) -> None:
        commands = "\n".join(self._queue)
        self._queue.clear()
        self._send_command(commands)

    def set_leg_angles(self, leg_index: int, coxa: float, femur: float, tibia: float) -> None:
        if leg_index not in range(6):
            raise ValueError("leg_index must be in range(6)")

        self.send_command(f"SET_LEG_ANGLES {leg_index} {coxa} {femur} {tibia}")

    def set_leg_position(self, leg_index: int, x: float, y: float, z: float) -> None:
        if leg_index not in range(6):
            raise ValueError("leg_index must be in range(6)")

        self.send_command(f"SET_LEG_POSITION {leg_index} {x} {y} {z}")

    def send_command(self, command: str) -> None:
        if not self._auto_send:
            return self._queue.append(command)

        self._send_command(command)

    def _send_command(self, command: str) -> None:
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
