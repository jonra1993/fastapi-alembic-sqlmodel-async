import os
import time
from collections.abc import Generator

API_EPOCH = 1640995200000

worker_id_bits = 5
process_id_bits = 5
max_worker_id = -1 ^ (-1 << worker_id_bits)
max_process_id = -1 ^ (-1 << process_id_bits)
sequence_bits = 12
process_id_shift = sequence_bits + worker_id_bits
worker_id_shift = sequence_bits
timestamp_left_shift = sequence_bits + worker_id_bits + process_id_bits
sequence_mask = -1 ^ (-1 << sequence_bits)


def snowflake_to_timestamp(_id):
    _id = _id >> 22
    _id += API_EPOCH
    _id /= 1000
    return _id


def generator(
    worker_id: int = 1,
    process_id: int = os.getpid() % 31,
    sleep=lambda x: time.sleep(x),
) -> Generator[int]:
    assert 0 <= worker_id <= max_worker_id
    assert 0 <= process_id <= max_process_id

    last_timestamp = -1
    sequence = 0

    while True:
        timestamp = int(time.time() * 1000)

        if last_timestamp > timestamp:
            sleep(last_timestamp - timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                sequence = -1 & sequence_mask
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp

        yield (
            ((timestamp - API_EPOCH) << timestamp_left_shift)
            | (process_id << process_id_shift)
            | (worker_id << worker_id_shift)
            | sequence
        )
