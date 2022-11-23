import grpc
from config.config import settings
from generated import HGW_pb2_grpc, HGW_pb2


class HGWClient(object):
    def __init__(self):
        HGW_address = '[::]:{}'.format(settings.HGW_PORT)
        self.channel = grpc.insecure_channel(HGW_address)
        self.register_stub = HGW_pb2_grpc.HGWRegisterStub(self.channel)

    async def StoreSD(self, ID, PID, r, K_G) -> HGW_pb2.StoreSDRes:
        request = HGW_pb2.StoreSDReq(ID=ID, PID=PID, r=r, K_G=K_G)
        response = self.register_stub.StoreSD(request)
        return response

    async def StoreMU(self, ID, PID, RID, K_G) -> HGW_pb2.StoreMURes:
        request = HGW_pb2.StoreMUReq(ID, PID, RID, K_G)
        response = self.register_stub.StoreMU(request)
        return response
