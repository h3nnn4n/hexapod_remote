from .gait import Gait, TripodGait
from .leg import Leg
from .serial import Serial


class Robot:
    legs: list[Leg]

    def __init__(self):
        self._serial = Serial()
        self._gait = TripodGait(self.serial)

        self.init_legs()
        self.update()

    def init_legs(self) -> None:
        self.legs = []

        for leg_id in range(6):
            leg = Leg(leg_id=leg_id, serial=self.serial)
            self.legs.append(leg)

    def init(self) -> None:
        self.serial.wait_for_ping()
        self.serial.enable_servos()

    def update(self) -> None:
        for leg in self.legs:
            leg.update_state()

    def walk(self, direction: float, distance: float) -> None:
        self.gait.walk(direction, distance)

    @property
    def gait(self) -> Gait:
        return self._gait

    @property
    def serial(self) -> Serial:
        return self._serial
