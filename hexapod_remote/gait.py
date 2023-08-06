import logging
from time import sleep

from .serial import Serial
from .vector import Vector


logger = logging.getLogger(__name__)


class Gait:
    def __init__(self, serial: Serial) -> None:
        self._serial = serial

    def walk(self, direction: float, distance: float) -> None:
        raise NotImplementedError


class TripodGait(Gait):
    def __init__(self, serial: Serial) -> None:
        super().__init__(serial)

        self.lhs_legs = [0, 1, 2]
        self.rhs_legs = [3, 4, 5]

        self.leg_group_1 = [0, 2, 4]
        self.leg_group_2 = [1, 3, 5]

        self.ground_height = -120.0
        self.feet_up_height = -75.0
        self.distance_from_body = 115.0
        self.stride_length = 70.0

        self.walk_speed = 150.0
        self.sleep_time = 0.4
        self.sleep_time2 = 0.4

    def walk(self, direction: float, distance: float) -> None:
        """Walk towards a `direction` for `distance` mm."""
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
        distance_left = distance

        n_steps = int(distance / stride_length)

        # convert from degrees to radians
        angle = direction * 3.1415952654 / 180.0
        walk_vector_pivot = Vector(0.0, distance_from_body)
        walk_vector_start = Vector().from_angle(angle, stride_length * 0.5) + walk_vector_pivot
        walk_vector_end = Vector().from_angle(angle, -stride_length * 0.5) + walk_vector_pivot

        serial.disable_auto_send()
        serial.set_legs_speed(self.walk_speed)
        serial.set_leg_mode("CONSTANT_SPEED")
        serial.send_commands()

        logger.info("starting")
        logger.info(f"{direction=} {distance=}")
        logger.info(f"{last_step_stride=} {n_steps=}")

        while distance_walked < distance:
            logger.info(f"{steps_taken=}  {distance_walked=}  {distance_left=}")
            if last_step_stride > 0 and distance - distance_walked < last_step_stride:
                logger.info("making last step with reduced stride")

                # FIXME: This needs to actually update the `walk_vector`s for it do so anything
                stride_length = last_step_stride

            if steps_taken % 2 == 0:
                for leg in self.leg_group_1:
                    serial.set_leg_position(leg, walk_vector_pivot.x, walk_vector_pivot.y, feet_up_height)

                for leg in self.leg_group_2:
                    if leg in self.rhs_legs:
                        x, y = walk_vector_start.as_tuple
                    else:
                        x, y = walk_vector_end.as_tuple

                    serial.set_leg_position(leg, x, y, ground_height)
                serial.send_commands()
                sleep(sleep_time)

                for leg in self.leg_group_1:
                    if leg in self.lhs_legs:
                        x, y = walk_vector_start.as_tuple
                    else:
                        x, y = walk_vector_end.as_tuple

                    serial.set_leg_position(leg, x, y, ground_height)
                serial.send_commands()
                sleep(sleep_time2)

                distance_walked += stride_length
                distance_left -= stride_length
            else:
                for leg in self.leg_group_2:
                    serial.set_leg_position(leg, walk_vector_pivot.x, walk_vector_pivot.y, feet_up_height)

                for leg in self.leg_group_1:
                    if leg in self.rhs_legs:
                        x, y = walk_vector_start.as_tuple
                    else:
                        x, y = walk_vector_end.as_tuple

                    serial.set_leg_position(leg, x, y, ground_height)
                serial.send_commands()
                sleep(sleep_time)

                for leg in self.leg_group_2:
                    if leg in self.lhs_legs:
                        x, y = walk_vector_start.as_tuple
                    else:
                        x, y = walk_vector_end.as_tuple

                    serial.set_leg_position(leg, x, y, ground_height)
                serial.send_commands()
                sleep(sleep_time2)

                distance_walked += stride_length
                distance_left -= stride_length
            steps_taken += 1

        logger.info(f"{steps_taken=}  {distance_walked=}  {distance_left=}")

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
