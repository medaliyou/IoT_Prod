from common.X import X
from common.Defines import *

import asyncio
import logging

import grpc

from common.base_logger import logger
from config.config import settings

"""
    gRPC Server
"""


async def serve() -> None:
    server = grpc.aio.server()

    listen_addr = '[::]:{}'.format(settings.MU_RPC_PORT)
    server.add_insecure_port(listen_addr)
    logger.info("Starting server on {}".format(listen_addr))

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
