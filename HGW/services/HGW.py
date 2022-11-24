# RA/server.py

from common.X import X
from common.base_logger import logger
import asyncio

import grpc
from config.config import settings

from generated import HGW_pb2_grpc
from services.HGWRegisterService import HGWRegisterService


async def serve() -> None:
    server = grpc.aio.server()

    HGW_pb2_grpc.add_HGWRegisterServicer_to_server(HGWRegisterService(), server)

    listen_addr = '[::]:{}'.format(settings.HGW_PORT)
    server.add_insecure_port(listen_addr)
    logger.info("Starting server on {}".format(listen_addr))
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
