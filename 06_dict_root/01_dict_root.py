import json
from ipaddress import IPv4Interface
from typing import Literal, Optional

from deepdiff import DeepDiff
from pydantic import BaseModel, Field, RootModel
from rich import print as pprint


class NetworkDevice(BaseModel):
    hostname: str = Field(min_length=1)
    role: str | list[str]
    addr: Optional[IPv4Interface | list[IPv4Interface] | Literal[""]] = None


class DynamicDict(RootModel[dict[str, NetworkDevice]]):
    pass


some_json = {
    "random1": {
        "hostname": "Switch-1",
        "role": ["core", "distribution"],
        "addr": ["192.168.1.1/24"],
    },
    "random2": {
        "hostname": "Switch-11",
        "role": "access",
        "addr": "192.168.2.1/24",
    },
    "random3": {
        "hostname": "Switch-88",
        "role": "core",
        "addr": "",
    },
}
devices = DynamicDict(some_json)

pprint(devices.model_dump_json(by_alias=True, exclude_none=True, indent=2))

# {
#     "random1": {
#         "hostname": "Switch-1",
#         "role": ["core", "distribution"],
#         "addr": ["192.168.1.1/24"],
#     },
#     "random2": {"hostname": "Switch-11", "role": "access", "addr": "192.168.2.1/24"},
#     "random3": {"hostname": "Switch-88", "role": "core", "addr": ""},
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

# No differences found between the JSON and the model dump.
