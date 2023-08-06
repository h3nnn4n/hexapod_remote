import argparse

from hexapod_remote.robot import Robot


def main(args) -> None:
    action = args.action

    robot = Robot()
    robot.init()

    match action:
        case "walk":
            robot.walk(args.direction, args.distance)
        case "idle":
            pass
        case _:
            print(f"got unknown {action=}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control the hexapod robot")
    parser.add_argument("action", action="store", type=str, help="Action to perform")
    parser.add_argument("--direction", required=False, default=0, type=int, help="Direction to walk, in degrees")
    parser.add_argument("--distance", required=False, default=100, type=int, help="Distance to walk, in mm")
    args = parser.parse_args()

    main(args)
