from enum import Enum as _Enum
from enum import auto  # noqa


class Enum(_Enum):
    @classmethod
    def from_string(self, string: str) -> _Enum:
        pass
