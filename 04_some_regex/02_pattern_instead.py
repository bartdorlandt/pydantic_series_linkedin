from typing import Literal, Optional

from pydantic import BaseModel, Field


class NetworkDevice(BaseModel):
    hostname: str = Field(min_length=1)
    type: Literal["EX4000", "EX4400"]
    purpose: list[Literal["core", "access", "distribution"]]
    rack: Optional[str] = None
    port: str = Field(default=None, pattern=r"^(xe|ge|et)-\d+/\d+/\d+(:\d+)?$")


class DeviceList(BaseModel):
    devices: list[NetworkDevice]


network_json = {
    "devices": [
        {
            "hostname": "Switch-1",
            "type": "EX4400",
            "purpose": ["core", "distribution"],
            "rack": "Rack-1",
            "port": "xe-0/0/0",
        },
        {
            "hostname": "Switch-11",
            "type": "EX4000",
            "purpose": ["access"],
            "port": "ge-0/0/0:0",
        },
    ]
}
devices = DeviceList(**network_json)

print(devices)
print(devices.devices[0].hostname)
print(devices.devices[0].port)
print(devices.model_dump_json(indent=2))

# devices = [
#     NetworkDevice(hostname="Switch-1", type="EX4400", purpose=["core", "distribution"], rack="Rack-1", port="xe-0/0/0"),
#     NetworkDevice(hostname="Switch-11", type="EX4000", purpose=["access"], rack=None, port="ge-0/0/0:0"),
# ]
# Switch - 1
# xe - 0 / 0 / 0
# {
#     "devices": [
#         {"hostname": "Switch-1", "type": "EX4400", "purpose": ["core", "distribution"], "rack": "Rack-1", "port": "xe-0/0/0"},
#         {"hostname": "Switch-11", "type": "EX4000", "purpose": ["access"], "rack": null, "port": "ge-0/0/0:0"},
#     ]
# }

from deepdiff import DeepDiff  # noqa: E402
from rich import print as pprint  # noqa: E402

if d := DeepDiff(network_json, devices.model_dump(by_alias=True, exclude_none=True), ignore_order=True):
    pprint(d)  # Should be empty if the JSON matches the model
else:
    print("No differences found between the JSON and the model dump.")

# No differences found between the JSON and the model dump.
