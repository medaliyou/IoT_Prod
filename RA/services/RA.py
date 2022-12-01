import asyncio
import grpc
from common.base_logger import logger
from config.config import settings
from generated import RA_pb2_grpc
from services.RAInitService import RAInitService
from services.RARegisterService import RARegisterService

"""
    gRPC Server
"""


async def serve() -> None:
    server = grpc.aio.server()
    RA_pb2_grpc.add_RAInitServicer_to_server(RAInitService(), server)
    RA_pb2_grpc.add_RARegisterServicer_to_server(RARegisterService(), server)

    listen_addr = '[::]:{}'.format(settings.RA_RPC_PORT)
    logger.info("Starting server on {}".format(listen_addr))

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
