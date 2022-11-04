#https://github.com/oittaa/uuid6-python
#https://github.com/uuid6/prototypes
r"""UUID draft version objects (universally unique identifiers).
This module provides the functions uuid6() and uuid7() for
generating version 6 and 7 UUIDs as specified in
https://github.com/uuid6/uuid6-ietf-draft.
"""

import os
import secrets
import time
from uuid import SafeUUID, UUID as UUID_
import timeit
from typing import Tuple


class UUID(UUID_):
    r"""UUID draft version objects"""

    def __init__(
        self,
        hex: str = None,
        bytes: bytes = None,
        bytes_le: bytes = None,
        fields: Tuple[int, int, int, int, int, int] = None,
        int: int = None,
        version: int = None,
        *,
        is_safe=SafeUUID.unknown
    ) -> None:
        r"""Create a UUID."""

        if int is None or [hex, bytes, bytes_le, fields].count(None) != 4:
            return super().__init__(
                hex=hex,
                bytes=bytes,
                bytes_le=bytes_le,
                fields=fields,
                int=int,
                version=version,
                is_safe=is_safe,
            )
        if not 0 <= int < 1 << 128:
            raise ValueError("int is out of range (need a 128-bit value)")
        if version is not None:
            if not 6 <= version <= 8:
                raise ValueError("illegal version number")
            # Set the variant to RFC 4122.
            int &= ~(0xC000 << 48)
            int |= 0x8000 << 48
            # Set the version number.
            int &= ~(0xF000 << 64)
            int |= version << 76
        
        super().__init__(int=int, is_safe=is_safe)

    @property
    def subsec(self) -> int:
        return ((self.int >> 64) & 0x0FFF) << 8 | ((self.int >> 54) & 0xFF)

    @property
    def time(self) -> int:
        if self.version == 6:
            return (
                (self.time_low << 28)
                | (self.time_mid << 12)
                | (self.time_hi_version & 0x0FFF)
            )
        if self.version == 7:
            return (self.int >> 80) * 10**6 + _subsec_decode(self.subsec)
        return super().time


def _subsec_decode(value: int) -> int:
    return -(-value * 10**6 // 2**20)

_last_v7_nano_timestamp = None
_last_v8_nano_timestamp = None

def uuid7() -> UUID:
    r"""UUID version 7 features a time-ordered value field derived from the
    widely implemented and well known Unix Epoch timestamp source, the
    number of milliseconds seconds since midnight 1 Jan 1970 UTC, leap
    seconds excluded.  As well as improved entropy characteristics over
    versions 1 or 6.
    Implementations SHOULD utilize UUID version 7 over UUID version 1 and
    6 if possible."""

    global _last_v7_nano_timestamp

    nanoseconds = time.time_ns()
    if _last_v7_nano_timestamp is not None and nanoseconds <= _last_v7_nano_timestamp:
        nanoseconds = _last_v7_nano_timestamp + 1
    _last_v7_nano_timestamp = nanoseconds
    timestamp_ms, timestamp_ns = divmod(nanoseconds, 10**6)
    rand = secrets.randbits(62)
    uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80  #unix_ts_ms 48 bits. Creates a 128bits variable y move the 48 bits MSB to the left 80 positions
    uuid_int |= (7 & 0B1111) << 76                    #ver 4 bits. UUID version
    uuid_int |= (nanoseconds & 0B111111111111) << 64  #rand_a 12bits
    uuid_int |= (4 & 0B11) << 62                      #variant 2 bits
    uuid_int |= rand                                  #rand_b 62 bits
    return UUID(int=uuid_int, version=7)

def uuid8() -> UUID:
    r"""UUID version 8 """

    global _last_v8_nano_timestamp

    nanoseconds = time.time_ns()
    if _last_v8_nano_timestamp is not None and nanoseconds <= _last_v8_nano_timestamp:
        nanoseconds = _last_v8_nano_timestamp + 1
    _last_v8_nano_timestamp = nanoseconds

    timestamp_ms, timestamp_ns = divmod(nanoseconds, 10**6)
    rand = secrets.randbits(62)
    uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80         #custom_a 48 bits. Creates a 128bits variable y move the 48 bits MSB to the left 80 positions
    uuid_int |= (8 & 0B1111) << 76                           #ver 4 bits. UUID version 4 bits
    uuid_int |= (os.getpid() & 0B111111111111) << 64         #custom_b 12bits
    uuid_int |= (4 & 0B11) << 62                             #variant 2 bits
    uuid_int |= rand                                         #custom_c 62 bits
    return UUID(int=uuid_int, version=8)