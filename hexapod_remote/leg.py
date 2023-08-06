from .enum import Enum, auto
from .serial import Serial
from .vector import Vector, Vector3d


class LegMode(Enum):
    INSTANTANEOUS = auto()
    CONSTANT_SPEED = auto()
    UNKNOWN = auto()


class Leg:
    leg_id: int
    current_position: Vector
    target_position: Vector
    final_position: Vector
    current_angles: Vector
    mode: LegMode
    error: float
    current_reach: float
    speed: float
    tolerance: float

    def __init__(self, leg_id: int, serial: Serial) -> None:
        self.leg_id = leg_id

        self.serial = serial

        self.current_position = Vector()
        self.target_position = Vector()
        self.final_position = Vector()
        self.current_angles = Vector()
        self.mode = LegMode.UNKNOWN
        self.error = float("-inf")
        self.current_reach = float("-inf")
        self.speed = float("-inf")
        self.tolerance = float("-inf")

        self.update_state()

    def update_state(self) -> None:
        raw_data = self.serial.send_read_command(f"READ_LEG_INFO {self.leg_id}")

        for line in raw_data:
            field, _, data = line.partition(":")
            field = field.strip()
            data = data.strip()

            match field:
                case "id":
                    if int(data) != self.leg_id:
                        print(f"got id={data} but expected {self.leg_id}")

                case "mode":
                    if data == "INSTANTANEOUS":
                        self.mode = LegMode.INSTANTANEOUS
                    elif data == "CONSTANT_SPEED":
                        self.mode = LegMode.CONSTANT_SPEED
                    else:
                        print(f"got UNKNOWN mode={data}")

                case "speed" | "tolerance" | "error" | "current_reach":
                    value = float(data)
                    setattr(self, field, value)

                case "current_position" | "target_position" | "final_position" | "current_angles":
                    x, y, z = data.split(",")

                    x = x.strip()
                    y = y.strip()
                    z = z.strip()

                    x = float(x)
                    y = float(y)
                    z = float(z)

                    value = Vector3d(x, y, z)

                case _:
                    if "READ_LEG_INFO" in field:
                        continue

                    print(f"got unknown field={field} with data={data}")
