from .gait import Gait, TripodGait
from .serial import Serial


class Robot:
    def __init__(self):
        self._serial = Serial()
        self._gait = TripodGait(self.serial)

    def init(self) -> None:
        self.serial.wait_for_ping()
        self.serial.enable_servos()

    def walk(self, direction: float, distance: float) -> None:
        self.gait.walk(direction, distance)

    @property
    def gait(self) -> Gait:
        return self._gait

    @property
    def serial(self) -> Serial:
        return self._serial
