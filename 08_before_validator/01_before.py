import json
from typing import Annotated

from deepdiff import DeepDiff
from pydantic import BaseModel, BeforeValidator, Field, RootModel
from rich import print as pprint


def turn_to_list_of_str(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [value]
    elif isinstance(value, list):
        return value
    else:
        raise ValueError(f"Expected str or list[str], got {type(value)}")


ListStr = Annotated[
    list[str],
    BeforeValidator(turn_to_list_of_str),
]


class NetworkDevice(BaseModel):
    hostname: str = Field(min_length=1)
    role: ListStr


class DynamicDict(RootModel[dict[str, NetworkDevice]]):
    pass


some_json = {
    "random1": {
        "hostname": "Switch-1",
        "role": ["core", "distribution"],
    },
    "random2": {
        "hostname": "Switch-11",
        "role": "access",
    },
    "random3": {
        "hostname": "Switch-88",
        "role": "core",
    },
}
devices = DynamicDict(some_json)

pprint(devices.model_dump_json(by_alias=True, exclude_none=True, indent=2))

# {
#   "random1": { "hostname": "Switch-1", "role": [ "core", "distribution" ] },
#   "random2": { "hostname": "Switch-11", "role": [ "access" ] },
#   "random3": { "hostname": "Switch-88", "role": [ "core" ] }
# }


dump = devices.model_dump_json(by_alias=True, exclude_none=True)
new = json.loads(dump)
if d := DeepDiff(
    some_json,
    new,
    ignore_order=True,
):
    pprint(d)  # Should be empty if the JSON matches the model
else:
    print("No differences found between the JSON and the model dump.")

# {
#     'type_changes': {
#         "root['random2']['role']": {
#             'old_type': <class 'str'>,
#             'new_type': <class 'list'>,
#             'old_value': 'access',
#             'new_value': ['access']
#         },
#         "root['random3']['role']": {
#             'old_type': <class 'str'>,
#             'new_type': <class 'list'>,
#             'old_value': 'core',
#             'new_value': ['core']
#         }
#     }
# }
