import logging
import grpc

from common.Defines import *
from common.X import X
from generated import RA_pb2_grpc, RA_pb2


class RAInitService(RA_pb2_grpc.RAInitServicer):

    async def GetID(self, request: RA_pb2.IDReq, context: grpc.aio.ServicerContext) -> RA_pb2.IDRes:
        logging.debug("Got GetID :")
        logging.debug(request)
        generated_ID = X(s=S_ID)
        response = RA_pb2.IDRes(ID=generated_ID.h, registered=False)
        return response
