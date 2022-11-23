import asyncio
import logging

import grpc

from common.Defines import *
from common.X import X
from common.base_logger import logger
from config.config import settings
from core.RA import RA
from generated import RA_pb2_grpc, RA_pb2
from services.InitService import InitService
from services.RegisterService import RegisterService

"""
    gRPC Server
"""

# Instantiate RA
RA_Instance = RA()


async def serve() -> None:
    server = grpc.aio.server()
    RA_pb2_grpc.add_RAInitServicer_to_server(InitService(), server)
    RA_pb2_grpc.add_RARegisterServicer_to_server(RegisterService(), server)

    listen_addr = '[::]:{}'.format(settings.RA_PORT)
    logger.info("Starting server on %s", listen_addr)

    server.add_insecure_port(listen_addr)

    await server.start()
    try:
        await server.wait_for_termination()
    except Exception as e:
        logger.error(e)
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)

if __name__ == '__main__':
    asyncio.run(serve())
