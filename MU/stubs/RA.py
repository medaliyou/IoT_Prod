import asyncio
import logging

import grpc

from common.Defines import *
from common.X import X
from common.base_logger import logger
from config.config import settings
from generated import RA_pb2_grpc, RA_pb2


class RAClient(object):
    def __init__(self):
        self.channel = None
        self.init_stub = None
        self.register_stub = None

        # RA_address = '[::]:{}'.format(settings.RA_PORT)
        # self.channel = grpc.insecure_channel(RA_address)
        # self.init_stub = RA_pb2_grpc.RAInitStub(self.channel)
        # self.register_stub = RA_pb2_grpc.RARegisterStub(self.channel)

    async def init_channel(self):
        try:
            RA_address = '{}:{}'.format(settings.RA_H, settings.RA_PORT)
            logger.warning(RA_address)
            self.channel = grpc.aio.insecure_channel(RA_address)
        except AttributeError as e:
            RA_address = '[::]:{}'.format(settings.RA_PORT)
            logger.warning(RA_address)
            self.channel = grpc.aio.insecure_channel(RA_address)

        try:
            await asyncio.wait_for(self.channel.channel_ready(), 1.0)
            self.init_stub = RA_pb2_grpc.RAInitStub(self.channel)
            self.register_stub = RA_pb2_grpc.RARegisterStub(self.channel)

        except asyncio.exceptions.TimeoutError as to:
            logger.error("Stub timeout, {}".format(to))
            self.init_stub = RA_pb2_grpc.RAInitStub(self.channel)
            self.register_stub = RA_pb2_grpc.RARegisterStub(self.channel)
        logger.info(self.init_stub)
        logger.info(self.register_stub)

    async def __check_and_create_channel(self):
        if self.init_stub is None or self.register_stub is None:
            await self.init_channel()

    async def GetID(self) -> RA_pb2.IDRes:
        # await self.__check_and_create_channel()
        try:
            request = RA_pb2.IDReq(deviceType=RA_pb2.DeviceType.SD, message="message")
            response = await self.init_stub.GetID(request, wait_for_ready=True)
            logger.info(response)
            return response

        except grpc.aio.AioRpcError as rpc_error:
            # assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            message = rpc_error
            logger.info("Client received: {}".format(message))

    async def RegisterSD(self, ID_SD, PID_SD, r_SD) -> RA_pb2.RegSDRes:
        # await self.__check_and_create_channel()
        try:
            request = RA_pb2.RegSDReq(ID=ID_SD, PID=PID_SD, r=r_SD)
            response = await self.register_stub.RegisterSD(request, wait_for_ready=True)
            return response

        except Exception as e:
            logger.info("Client received: {}".format(e))

    async def RegisterMU(self, ID_MU, PID_MU) -> RA_pb2.RegMURes:
        # await self.__check_and_create_channel()
        try:
            request = RA_pb2.RegMUReq(ID=ID_MU, PID=PID_MU)
            response = await self.register_stub.RegisterMU(request, wait_for_ready=True)
            return response
        except Exception as e:
            logger.info("Client received: {}".format(e))


RA_Client: RAClient = None


async def cRAClient() -> RAClient:
    global RA_Client
    if RA_Client is None:
        RA_Client = RAClient()
        await RA_Client.init_channel()

    return RA_Client
