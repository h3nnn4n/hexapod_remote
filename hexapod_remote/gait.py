import logging
from time import sleep

from .serial import Serial


logger = logging.getLogger(__name__)


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

        self.ground_height = -120.0
        self.feet_up_height = -75.0
        self.distance_from_body = 95.0
        self.stride_length = 40.0

        self.walk_speed = 150.0
        self.sleep_time = 0.75
        self.sleep_time2 = 0.5

    def walk(self, direction: float, distance: float) -> None:
        """Walk towards a `direction` for `distance` mm."""
        # TODO: Rotate movement vectors based on `direction`
        # TODO: Adapt stride length based on `distance` to avoid doing one
        # extra step at the end

        serial = self.serial

        ground_height = self.ground_height
        feet_up_height = self.feet_up_height
        distance_from_body = self.distance_from_body
        stride_length = self.stride_length

        sleep_time = self.sleep_time
        sleep_time2 = self.sleep_time2

        last_step_stride = distance % stride_length
        distance_walked = 0.0
        steps_taken = 0

        serial.disable_auto_send()
        serial.set_legs_speed(self.walk_speed)
        serial.set_leg_mode("CONSTANT_SPEED")
        serial.send_commands()

        logger.info("starting")

        while distance_walked < distance:
            logger.info(f"{steps_taken=}  {distance_walked=}  {distance=}  {last_step_stride=}")
            if last_step_stride > 0 and distance_walked - distance < last_step_stride:
                stride_length = last_step_stride

            if steps_taken % 2 == 0:
                for leg in self.leg_group_1:
                    serial.set_leg_position(leg, 0, distance_from_body, feet_up_height)

                for leg in self.leg_group_2:
                    serial.set_leg_position(leg, stride_length, distance_from_body, ground_height)
                serial.send_commands()
                sleep(sleep_time)

                for leg in self.leg_group_1:
                    serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
                serial.send_commands()
                sleep(sleep_time2)

                distance_walked += stride_length
            else:
                for leg in self.leg_group_2:
                    serial.set_leg_position(leg, 0, distance_from_body, feet_up_height)

                for leg in self.leg_group_1:
                    serial.set_leg_position(leg, stride_length, distance_from_body, ground_height)
                serial.send_commands()
                sleep(sleep_time)

                for leg in self.leg_group_2:
                    serial.set_leg_position(leg, -stride_length, distance_from_body, ground_height)
                serial.send_commands()
                sleep(sleep_time2)

                distance_walked += stride_length
            steps_taken += 1

        self.stop_walking()

    def stop_walking(self) -> None:
        """Safely move legs to resting position after walk cycle ends."""
        sleep_time = 0.25
        leg_up_height = 20

        logger.info("stopping")
        for leg in self.leg_group_1:
            self.serial.set_leg_position(leg, 0, self.distance_from_body, self.ground_height + leg_up_height)
        self.serial.send_commands()
        sleep(sleep_time)

        for leg in self.leg_group_1:
            self.serial.set_leg_position(leg, 0, self.distance_from_body, self.ground_height)
        self.serial.send_commands()
        sleep(sleep_time)

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
