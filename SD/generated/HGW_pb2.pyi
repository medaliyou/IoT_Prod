from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthKES1Req(_message.Message):
    __slots__ = ["C1", "M1", "PID", "V"]
    C1: str
    C1_FIELD_NUMBER: _ClassVar[int]
    M1: str
    M1_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    V: str
    V_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, PID: _Optional[str] = ..., M1: _Optional[str] = ..., C1: _Optional[str] = ..., V: _Optional[str] = ...) -> None: ...

class AuthKES4Res(_message.Message):
    __slots__ = ["M5", "V_G"]
    M5: str
    M5_FIELD_NUMBER: _ClassVar[int]
    V_G: str
    V_G_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, M5: _Optional[str] = ..., V_G: _Optional[str] = ...) -> None: ...

class AuthKES6Req(_message.Message):
    __slots__ = ["M6", "PID"]
    M6: str
    M6_FIELD_NUMBER: _ClassVar[int]
    PID: str
    PID_FIELD_NUMBER: _ClassVar[int]
    def __init__(self, M6: _Optional[str] = ..., PID: _Optional[str] = ...) -> None: ...

class AuthKES6Res(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

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
