from typing import Annotated, Literal, Optional

from netaddr import EUI, AddrFormatError
from pydantic import AfterValidator, BaseModel, Field, PlainSerializer

IntStr = Annotated[
    int,
    PlainSerializer(lambda x: str(x), return_type=str, when_used="always"),
]


def mac_address_validator(value: str) -> str:
    try:
        EUI(value)
    except AddrFormatError as e:
        raise ValueError(f"Invalid MAC address: {value}") from e
    return value


MacAddress = Annotated[
    str,
    AfterValidator(mac_address_validator),
]


class NetworkDevice(BaseModel):
    instance_id: IntStr = Field(alias="instance-id")
    hostname: str = Field(min_length=1)
    type: Literal["EX4000", "EX4400"]
    purpose: list[Literal["core", "access", "distribution"]]
    rack: Optional[str] = None
    mac: MacAddress


class DeviceList(BaseModel):
    devices: list[NetworkDevice]


network_json = {
    "devices": [
        {
            "instance-id": "151",
            "hostname": "Switch-1",
            "type": "EX4400",
            "purpose": ["core", "distribution"],
            "rack": "Rack-1",
            "mac": "00:1A:2B:3C:4D:5E",
        },
        {
            "instance-id": "263",
            "hostname": "Switch-11",
            "type": "EX4000",
            "purpose": ["access"],
            "mac": "00:1A:2B:3C:4D:5F",
        },
    ]
}
devices = DeviceList(**network_json)

print(devices)
print(devices.devices[0].hostname)
print(devices.devices[0].mac)
print(devices.model_dump_json(indent=2))

# devices=[NetworkDevice(hostname='Switch-1', instance_id=151, mac='00:1A:2B:3C:4D:5E', purpose=['core', 'distribution'], rack='Rack-1', type='EX4400'),
# NetworkDevice(hostname='Switch-11', instance_id=263, mac='00:1A:2B:3C:4D:5F', purpose=['access'], rack=None, type='EX4000')]
# Switch-1
# 00:1A:2B:3C:4D:5E
# {
#   "devices": [
#     {
#       "hostname": "Switch-1",
#       "instance_id": "151",
#       "mac": "00:1A:2B:3C:4D:5E",
#       "purpose": [
#         "core",
#         "distribution"
#       ],
#       "rack": "Rack-1",
#       "type": "EX4400"
#     },
#     {
#       "hostname": "Switch-11",
#       "instance_id": "263",
#       "mac": "00:1A:2B:3C:4D:5F",
#       "purpose": [
#         "access"
#       ],
#       "rack": null,
#       "type": "EX4000"
#     }
#   ]
# }


# from deepdiff import DeepDiff
# from rich import print as pprint

# d = DeepDiff(
#     network_json,
#     devices.model_dump(),
#     ignore_order=True,
# )

# pprint(d)  # Should be empty if the JSON matches the model

# {
#     'values_changed': {
#         "root['devices'][1]": {
#             'new_value': {'instance_id': '263', 'hostname': 'Switch-11', 'type': 'EX4000', 'purpose': ['access'], 'rack': None, 'mac': '00:1A:2B:3C:4D:5F'},
#             'old_value': {'instance-id': '263', 'hostname': 'Switch-11', 'type': 'EX4000', 'purpose': ['access'], 'mac': '00:1A:2B:3C:4D:5F'}
#         },
#         "root['devices'][0]": {
#             'new_value': {'instance_id': '151', 'hostname': 'Switch-1', 'type': 'EX4400', 'purpose': ['core', 'distribution'], 'rack': 'Rack-1', 'mac': '00:1A:2B:3C:4D:5E'},
#             'old_value': {'instance-id': '151', 'hostname': 'Switch-1', 'type': 'EX4400', 'purpose': ['core', 'distribution'], 'rack': 'Rack-1', 'mac': '00:1A:2B:3C:4D:5E'}
#         }
#     }
# }


from deepdiff import DeepDiff  # noqa: E402
from rich import print as pprint  # noqa: E402

if d := DeepDiff(network_json, devices.model_dump(by_alias=True, exclude_none=True), ignore_order=True):
    pprint(d)  # Should be empty if the JSON matches the model
else:
    print("No differences found between the JSON and the model dump.")

# No differences found between the JSON and the model dump.
