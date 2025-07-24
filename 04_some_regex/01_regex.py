import re
from typing import Annotated

from pydantic import AfterValidator


def port_validator(value: str) -> str:
    port_re = re.compile(r"^(xe|ge|et)-\d+/\d+/\d+(:\d+)?$")

    if not isinstance(value, str):
        raise TypeError("Port name must be a string")
    elif not value:
        raise ValueError("Invalid port name")
    elif not port_re.match(value):
        raise ValueError(f"Invalid port name: {value}")

    return value


Port = Annotated[
    str,
    AfterValidator(port_validator),
]
