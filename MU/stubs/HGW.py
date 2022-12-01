import asyncio

import grpc

from common.base_logger import logger
from config.config import settings
from generated import HGW_pb2_grpc, HGW_pb2


class HGWClient(object):
    def __init__(self):
        self.channel = None
        self.register_stub = None
        self.auth_KE_stub = None

        # HGW_address = '[::]:{}'.format(settings.HGW_PORT)
        # self.channel = grpc.insecure_channel(HGW_address)
        # self.register_stub = HGW_pb2_grpc.HGWRegisterStub(self.channel)

    async def init_channel(self):

        try:
            if settings.HGW_H is not None:
                HGW_address = '{}:{}'.format(settings.HGW_H, settings.HGW_RPC_PORT)
                logger.warning(HGW_address)
                self.channel = grpc.aio.insecure_channel(HGW_address)
            else:
                HGW_address = '[::]:{}'.format(settings.HGW_RPC_PORT)
                logger.warning(HGW_address)
                self.channel = grpc.aio.insecure_channel(HGW_address)

        except AttributeError as e:
            HGW_address = '[::]:{}'.format(settings.HGW_RPC_PORT)
            logger.warning(HGW_address)
            self.channel = grpc.aio.insecure_channel(HGW_address)

        try:
            await asyncio.wait_for(self.channel.channel_ready(), 1.0)
            self.register_stub = HGW_pb2_grpc.HGWRegisterStub(self.channel)
            self.auth_KE_stub = HGW_pb2_grpc.HGWAuthKEStub(self.channel)
        except asyncio.exceptions.TimeoutError as to:
            logger.error("Stub timeout, {}".format(to))
            self.register_stub = HGW_pb2_grpc.HGWRegisterStub(self.channel)
            self.auth_KE_stub = HGW_pb2_grpc.HGWAuthKEStub(self.channel)

    async def __check_and_create_channel(self):
        if self.register_stub is None:
            await self.register_stub()

    async def StoreSD(self, ID, PID, r, K_G) -> HGW_pb2.StoreSDRes:
        # await self.__check_and_create_channel()
        try:
            request = HGW_pb2.StoreSDReq(ID=ID, PID=PID, r=r, K_G=K_G)
            response = await self.register_stub.StoreSD(request, wait_for_ready=True)
            logger.info("HGW_stub = {}".format(response))
            return response

        except grpc.aio.AioRpcError as rpc_error:
            # assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            message = rpc_error
            logger.info("Client received: {}".format(message))
            return response
        except Exception as e:
            logger.error(e)

    async def StoreMU(self, ID, PID, RID, K_G, PID_n=None, RID_n=None) -> HGW_pb2.StoreMURes:
        # await self.__check_and_create_channel()
        logger.debug(ID)
        logger.debug(PID)
        logger.debug(RID)
        logger.debug(K_G)
        logger.debug(PID_n)
        logger.debug(RID_n)

        request = HGW_pb2.StoreMUReq(ID=ID, PID=PID, RID=RID, K_G=K_G, PID_n=PID_n, RID_n=RID_n)
        try:
            response = await self.register_stub.StoreMU(request, wait_for_ready=True)
            logger.info(response)

            return response
        except grpc.aio.AioRpcError as rpc_error:
            # assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            message = rpc_error
            logger.info("Client received: {}".format(message))
            return response
        except Exception as e:
            logger.error(e)

    async def AuthKES1(self, PID_MU, M1, C1, V_MU) -> HGW_pb2.AuthKES4Res:
        request = HGW_pb2.AuthKES1Req(PID=PID_MU, M1=M1, C1=C1, V=V_MU)

        try:
            response: HGW_pb2.AuthKES4Res = await self.auth_KE_stub.AuthKES1(request, wait_for_ready=True)
            logger.info(response)

            return response
        except grpc.aio.AioRpcError as rpc_error:
            # assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            message = rpc_error
            logger.error("Client received: {}".format(message))
        except Exception as e:
            logger.error(e)

    async def AuthKES6(self, M6, PID_MU) -> HGW_pb2.AuthKES6Res:
        request = HGW_pb2.AuthKES6Req(M6=M6, PID=PID_MU)

        try:
            response: HGW_pb2.AuthKES6Res = await self.auth_KE_stub.AuthKES6(request, wait_for_ready=True)
            logger.info(response)

            return response
        except grpc.aio.AioRpcError as rpc_error:
            # assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            message = rpc_error
            logger.info("Client received: {}".format(message))
            return response
        except Exception as e:
            logger.error(e)


HGW_Client: HGWClient = None


async def cHGWClient() -> HGWClient:
    global HGW_Client
    if HGW_Client is None:
        HGW_Client = HGWClient()
        await HGW_Client.init_channel()

    return HGW_Client
