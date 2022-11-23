# RA/server.py


from Common.X import X
from Common.Defines import *

import asyncio
import logging

import grpc

from generated import RA_pb2
from generated import RA_pb2_grpc

from Common.base_logger import logger
from core import HGW
from config.config import settings


"""
    Init Phase
"""


class RAInitService(RA_pb2_grpc.RAInitServicer):

    async def GetID(self, request: RA_pb2.IDReq, context: grpc.aio.ServicerContext) -> RA_pb2.IDRes:
        logging.debug("Got GetID :")
        logging.debug(request)

        generated_ID = X(s=S_ID)
        response = RA_pb2.IDRes(ID=generated_ID.h, registered=False)
        return response


"""
    Registration Phase
"""


class RARegService(RA_pb2_grpc.RARegisterServicer):

    async def RegisterSD(self, request: RA_pb2.RegSDReq, context: grpc.aio.ServicerContext) -> RA_pb2.RegSDRes:
        logging.debug("Got Register SD :")
        logging.debug(request)
        _K_G_SD = await RA_Instance.registerSD(ID_SD=request.ID, PID_SD=request.PID, r_SD=request.r)
        response = RA_pb2.RegSDRes(K_G=_K_G_SD.h)
        return response

    async def RegisterMU(self, request: RA_pb2.RegMUReq, context: grpc.aio.ServicerContext) -> RA_pb2.RegMURes:
        logging.debug("Got Register SD :")
        logging.debug(request)
        _K_G_MU, _RID_MU = await RA_Instance.registerMU(ID_MU=request.ID, PID_MU=request.PID)
        response = RA_pb2.RegMURes(K_G=_K_G_MU.h, RID=_RID_MU.h)
        return response


"""
    gRPC Server
"""

# Instantiate RA
RA_Instance = RA()


async def serve() -> None:
    server = grpc.aio.server()
    RA_pb2_grpc.add_RAInitServicer_to_server(RAInitService(), server)
    RA_pb2_grpc.add_RARegisterServicer_to_server(RARegService(), server)

    listen_addr = '[::]:{}'.format(settings.RA_PORT)
    server.add_insecure_port(listen_addr)
    logger.info("Starting server on %s", listen_addr)

    await server.start()
    try:
        await server.wait_for_termination()
    except Exception as e:
        logging.error(e)
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(serve())
