import json
from ipaddress import IPv4Interface
from typing import Optional

from deepdiff import DeepDiff
from pydantic import BaseModel, Field
from rich import print as pprint

some_json = {
    "devices": {
        "rtr1": {
            "hostname": "Router-1",
            "role": ["core"],
            "addr": "192.168.1.1/24",
            "monitor": True,
        },
        "newrtr2": {
            "hostname": "Router-2",
            "role": ["core"],
            "addr": "192.168.1.2/24",
            "monitor": False,
        },
        "switch1": {
            "hostname": "Switch-1",
            "role": ["access"],
            "addr": "192.168.10.1/24",
            "id": 532,
        },
        "switch2": {
            "hostname": "Switch-2",
            "role": ["access"],
            "addr": "192.168.10.2/24",
            "id": 321,
        },
        "console1": {
            "hostname": "Console-1",
            "role": ["management"],
            "addr": "172.16.0.1/24",
            "instance-id": 456,
        },
        "console2": {
            "hostname": "Console-2",
            "role": ["management"],
            "addr": "172.16.0.2/24",
        },
    },
}


class NetworkDevice(BaseModel):
    hostname: str = Field(min_length=1)
    role: list[str]
    addr: IPv4Interface


class NetworkDeviceRtr(NetworkDevice):
    monitor: bool


class NetworkDeviceNewRtr(BaseModel):
    hostname: str = Field(min_length=1)
    role: list[str]
    addr: IPv4Interface
    monitor: bool


class NetworkDeviceSwitch(NetworkDevice):
    id: int


class NetworkDeviceConsole(NetworkDevice):
    instance_id: Optional[int] = Field(None, alias="instance-id")


class DeviceList(BaseModel):
    devices: dict[
        str,
        NetworkDeviceNewRtr | NetworkDeviceConsole | NetworkDeviceSwitch | NetworkDeviceRtr,
    ]


devices = DeviceList(**some_json)
pprint(devices.model_dump_json(by_alias=True, exclude_none=True, indent=2))

# {
#   "devices": {
#     "rtr1": { "hostname": "Router-1", "role": [ "core" ], "addr": "192.168.1.1/24", "monitor": true },
#     "newrtr2": { "hostname": "Router-2", "role": [ "core" ], "addr": "192.168.1.2/24", "monitor": false },
#     "switch1": { "hostname": "Switch-1", "role": [ "access" ], "addr": "192.168.10.1/24", "id": 532 },
#     "switch2": { "hostname": "Switch-2", "role": [ "access" ], "addr": "192.168.10.2/24", "id": 321 },
#     "console1": { "hostname": "Console-1", "role": [ "management" ], "addr": "172.16.0.1/24", "instance-id": 456 },
#     "console2": { "hostname": "Console-2", "role": [ "management" ], "addr": "172.16.0.2/24" }
#     }
#   }
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
