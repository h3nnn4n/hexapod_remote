import contextlib
import logging.config

import yaml
from decouple import config


with contextlib.suppress(Exception), open("logging.yaml", "rt") as f:
    dict_config = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_config)


SERIAL_PORT: str = str(config("SERIAL_PORT", default="/dev/ttyUSB0", cast=str))
BAUD_RATE: int = int(config("BAUD_RATE", default=115200, cast=int))
SERIAL_TIMEOUT: float = float(config("SERIAL_TIMEOUT", default=0.01, cast=float))
