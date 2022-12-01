import asyncio

import grpc

from common.base_logger import logger
from config.config import settings
from generated import SD_pb2, SD_pb2_grpc


class SDClient(object):
    def __init__(self):
        self.channel = None
        self.auth_KE_stub = None

        # RA_address = '[::]:{}'.format(settings.RA_PORT)
        # self.channel = grpc.insecure_channel(RA_address)
        # self.init_stub = RA_pb2_grpc.RAInitStub(self.channel)
        # self.register_stub = RA_pb2_grpc.RARegisterStub(self.channel)

    async def init_channel(self):
        try:
            if settings.SD_H is not None:

                SD_address = '{}:{}'.format(settings.SD_H, settings.SD_RPC_PORT)
                logger.warning(SD_address)
                self.channel = grpc.aio.insecure_channel(SD_address)
            else:
                SD_address = '[::]:{}'.format(settings.SD_RPC_PORT)
                logger.warning(SD_address)
                self.channel = grpc.aio.insecure_channel(SD_address)

        except AttributeError as e:
            SD_address = '[::]:{}'.format(settings.SD_RPC_PORT)
            logger.warning(SD_address)
            self.channel = grpc.aio.insecure_channel(SD_address)

        try:
            await asyncio.wait_for(self.channel.channel_ready(), 1.0)
            self.auth_KE_stub = SD_pb2_grpc.SDAuthKEStub(self.channel)
        except asyncio.exceptions.TimeoutError as to:
            logger.error("Stub timeout, {}".format(to))
            self.auth_KE_stub = SD_pb2_grpc.SDAuthKEStub(self.channel)
        logger.info(self.auth_KE_stub)

    async def __check_and_create_channel(self):
        if self.init_stub is None or self.register_stub is None:
            await self.init_channel()

    async def AuthKES3(self, PID_MU, M3, C2, V_G_MU) -> SD_pb2.AuthKES3Res:
        # await self.__check_and_create_channel()
        try:
            request = SD_pb2.AuthKES3Req(PID=PID_MU, M3=M3, C2=C2, V=V_G_MU)
            response = await self.auth_KE_stub.AuthKES3(request, wait_for_ready=True)
            return response

        except Exception as e:
            # assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            message = e
            logger.info("Client received: {}".format(e))


SD_Client: SDClient = None


async def cSDClient() -> SDClient:
    global SD_Client
    if SD_Client is None:
        SD_Client = SDClient()
        await SD_Client.init_channel()

    return SD_Client
