import json
from ipaddress import IPv4Interface
from typing import Literal, Optional

from deepdiff import DeepDiff
from pydantic import BaseModel, Field
from rich import print as pprint


class NetworkDevice(BaseModel):
    hostname: str = Field(min_length=1)
    role: str | list[str]
    addr: Optional[IPv4Interface | list[IPv4Interface] | Literal[""]] = None


class DeviceList(BaseModel):
    devices: list[NetworkDevice]


network_json = {
    "devices": [
        {
            "hostname": "Switch-1",
            "role": ["core", "distribution"],
            "addr": ["192.168.1.1/24"],
        },
        {
            "hostname": "Switch-11",
            "role": "access",
            "addr": "192.168.2.1/24",
        },
        {
            "hostname": "Switch-88",
            "role": "core",
            "addr": "",
        },
    ]
}
devices = DeviceList(**network_json)

pprint(devices.model_dump_json(by_alias=True, exclude_none=True, indent=2))

# {
#     "devices": [
#         {
#             "hostname": "Switch-1",
#             "role": ["core", "distribution"],
#             "addr": ["192.168.1.1/24"],
#         },
#         {"hostname": "Switch-11", "role": "access", "addr": "192.168.2.1/24"},
#         {"hostname": "Switch-88", "role": "core", "addr": ""},
#     ]
# }

dump = devices.model_dump_json(by_alias=True, exclude_none=True)
new = json.loads(dump)
d = DeepDiff(
    network_json,
    new,
    ignore_order=True,
)

if d:
    pprint(d)  # Should be empty if the JSON matches the model
else:
    print("No differences found between the JSON and the model dump.")

# No differences found between the JSON and the model dump.
