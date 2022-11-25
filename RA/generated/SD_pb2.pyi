from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthKES3Req(_message.Message):
    __slots__ = ["C2", "M3", "PID", "V"]
    C2: str
    C2_FIELD_NUMBER: _ClassVar[int]
    M3: str
    M3_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    V: str
    V_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, PID: _Optional[str] = ..., M3: _Optional[str] = ..., C2: _Optional[str] = ..., V: _Optional[str] = ...) -> None: ...

class AuthKES3Res(_message.Message):
    __slots__ = ["M4", "V"]
    M4: str
    M4_FIELD_NUMBER: _ClassVar[int]
    V: str
    V_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, M4: _Optional[str] = ..., V: _Optional[str] = ...) -> None: ...
