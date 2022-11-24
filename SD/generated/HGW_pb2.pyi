from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StoreMUReq(_message.Message):
    __slots__ = ["ID", "K_G", "PID", "PID_n", "RID", "RID_n"]
    ID: str
    ID_FIELD_NUMBER: _ClassVar[int]
    K_G: str
    K_G_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    PID_N_FIELD_NUMBER: _ClassVar[int]
    PID_n: str
    RID: str
    RID_FIELD_NUMBER: _ClassVar[int]
    RID_N_FIELD_NUMBER: _ClassVar[int]
    RID_n: str
    def __init__(self, ID: _Optional[str] = ..., PID: _Optional[str] = ..., RID: _Optional[str] = ..., K_G: _Optional[str] = ..., PID_n: _Optional[str] = ..., RID_n: _Optional[str] = ...) -> None: ...

class StoreMURes(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class StoreSDReq(_message.Message):
    __slots__ = ["ID", "K_G", "PID", "r"]
    ID: str
    ID_FIELD_NUMBER: _ClassVar[int]
    K_G: str
    K_G_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    r: str
    def __init__(self, ID: _Optional[str] = ..., PID: _Optional[str] = ..., r: _Optional[str] = ..., K_G: _Optional[str] = ...) -> None: ...

class StoreSDRes(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
