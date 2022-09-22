# https://github.com/tiangolo/sqlmodel/issues/159
from functools import partial
import re

_snake_1 = partial(re.compile(r'(.)((?<![^A-Za-z])[A-Z][a-z]+)').sub, r'\1_\2')
_snake_2 = partial(re.compile(r'([a-z0-9])([A-Z])').sub, r'\1_\2')


def snake_case(string: str) -> str:
    return _snake_2(_snake_1(string)).casefold()