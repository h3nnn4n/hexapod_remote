from time import sleep

from .serial import Serial


class Gait:
    def __init__(self, serial: Serial) -> None:
        self._serial = serial

    def walk(self, direction: float, distance: float) -> None:
        raise NotImplementedError


class TripodGait(Gait):
    def __init__(self, serial: Serial) -> None:
        super().__init__(serial)

        self.leg_group_1 = [0, 2, 4]
        self.leg_group_2 = [1, 3, 5]

        self.ground_height = -120
        self.feet_up_height = -75
        self.distance_from_body = 95
        self.stride_length = 40

        self.walk_speed = 150
        self.sleep_time = 0.75
        self.sleep_time2 = 0.5

    def walk(self, direction: float, distance: float) -> None:
        """Walk towards a `direction` for `distance` mm."""
        # TODO: Rotate movement vectors based on `direction`
        # TODO: Calculate number of steps based on `distance`

        serial = self.serial

        ground_height = self.ground_height
        feet_up_height = self.feet_up_height
        distance_from_body = self.distance_from_body
        stride_length = self.stride_length

        sleep_time = self.sleep_time
        sleep_time2 = self.sleep_time2

        serial.disable_auto_send()
        serial.set_legs_speed(self.walk_speed)
        serial.set_leg_mode("CONSTANT_SPEED")
        serial.send_commands()

        while True:
            # Part 1
            for leg in self.leg_group_1:
                serial.set_leg_position(leg, 0, distance_from_body, feet_up_height)

            for leg in self.leg_group_2:
                serial.set_leg_position(leg, stride_length, distance_from_body, ground_height)
            serial.send_commands()
            sleep(sleep_time)
            print()

            for leg in self.leg_group_1:
                serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
            serial.send_commands()
            sleep(sleep_time2)
            print()

            # Part 2
            for leg in self.leg_group_2:
                serial.set_leg_position(leg, 0, distance_from_body, feet_up_height)

            for leg in self.leg_group_1:
                serial.set_leg_position(leg, stride_length, distance_from_body, ground_height)
            serial.send_commands()
            sleep(sleep_time)
            print()

            for leg in self.leg_group_2:
                serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
            serial.send_commands()
            sleep(sleep_time2)
            print()

            break

        self.stop_walking()

    def stop_walking(self) -> None:
        """Safely move legs to resting position after walk cycle ends."""
        sleep_time = 0.25
        leg_up_height = 20

        print("stopping")
        for leg in self.leg_group_1:
            self.serial.set_leg_position(leg, 0, self.distance_from_body, self.ground_height + leg_up_height)
        self.serial.send_commands()
        sleep(sleep_time)

        for leg in self.leg_group_1:
            self.serial.set_leg_position(leg, 0, self.distance_from_body, self.ground_height)
        self.serial.send_commands()
        sleep(sleep_time)
        print()

        for leg in self.leg_group_2:
            self.serial.set_leg_position(leg, 0, self.distance_from_body, self.ground_height + leg_up_height)
        self.serial.send_commands()
        sleep(sleep_time)

        for leg in self.leg_group_2:
            self.serial.set_leg_position(leg, 0, self.distance_from_body, self.ground_height)
        self.serial.send_commands()
        sleep(sleep_time)

    @property
    def serial(self) -> Serial:
        return self._serial
