from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
MU: DeviceType
SD: DeviceType

class IDReq(_message.Message):
    __slots__ = ["deviceType", "message"]
    DEVICETYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    deviceType: DeviceType
    message: str
    def __init__(self, deviceType: _Optional[_Union[DeviceType, str]] = ..., message: _Optional[str] = ...) -> None: ...

class IDRes(_message.Message):
    __slots__ = ["ID", "registered"]
    ID: str
    ID_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_FIELD_NUMBER: _ClassVar[int]
    registered: bool
    def __init__(self, ID: _Optional[str] = ..., registered: bool = ...) -> None: ...

class RegMUReq(_message.Message):
    __slots__ = ["ID", "PID"]
    ID: str
    ID_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, ID: _Optional[str] = ..., PID: _Optional[str] = ...) -> None: ...

class RegMURes(_message.Message):
    __slots__ = ["K_G", "RID"]
    K_G: str
    K_G_FIELD_NUMBER: _ClassVar[int]
    RID: str
    RID_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, K_G: _Optional[str] = ..., RID: _Optional[str] = ...) -> None: ...

class RegSDReq(_message.Message):
    __slots__ = ["ID", "PID", "r"]
    ID: str
    ID_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    r: str
    def __init__(self, ID: _Optional[str] = ..., PID: _Optional[str] = ..., r: _Optional[str] = ...) -> None: ...

class RegSDRes(_message.Message):
    __slots__ = ["K_G"]
    K_G: str
    K_G_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, K_G: _Optional[str] = ...) -> None: ...

class DeviceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
