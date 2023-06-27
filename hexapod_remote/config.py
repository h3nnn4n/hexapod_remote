from decouple import config


SERIAL_PORT = config("SERIAL_PORT", default="/dev/ttyUSB0")
BAUD_RATE = config("BAUD_RATE", default=115200)
SERIAL_TIMEOUT = config("SERIAL_TIMEOUT", default=0.01, cast=float)
