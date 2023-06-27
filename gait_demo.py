#!/usr/bin/env python3

from hexapod_remote.serial import Serial

from time import sleep


def main():
    serial = Serial()
    serial.wait_for_ping()


if __name__ == "__main__":
    main()
