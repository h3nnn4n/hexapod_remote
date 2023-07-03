import argparse

from hexapod_remote.robot import Robot


def main(args) -> None:
    robot = Robot()
    robot.init()
    robot.walk(args.direction, args.distance)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control the hexapod robot")
    parser.add_argument("walk", type=str, help="Action to perform")
    parser.add_argument("--direction", required=False, default=0, type=int, help="Direction to walk, in degrees")
    parser.add_argument("--distance", required=False, default=100, type=int, help="Distance to walk, in mm")
    args = parser.parse_args()

    main(args)
