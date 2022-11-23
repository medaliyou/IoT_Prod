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

    async def init_channel(self):
        RA_address = '[::]:{}'.format(settings.RA_PORT)
        # self.channel = grpc.insecure_channel(RA_address)
        self.channel = grpc.aio.insecure_channel(RA_address)
        await asyncio.wait_for(self.channel.channel_ready(), 3.0)
        self.init_stub = RA_pb2_grpc.RAInitStub(self.channel)
        self.register_stub = RA_pb2_grpc.RARegisterStub(self.channel)
        logger.info(self.init_stub)
        logger.info(self.register_stub)

    async def GetID(self) -> RA_pb2.IDRes:
        response = await self.init_stub.GetID(RA_pb2.IDReq(deviceType=RA_pb2.DeviceType.SD, message="message"))
        return response

    async def RegisterSD(self, ID_SD) -> RA_pb2.RegSDRes:
        response = await self.register_stub.RegisterSD(RA_pb2.RegSDReq(ID=ID_SD, PID=X(s=S_KEY).h, r=X(s=S_KEY).h))
        return response
