import logging
import grpc

from core.RA import RA
from generated import RA_pb2_grpc, RA_pb2


class RegisterService(RA_pb2_grpc.RARegisterServicer):

    async def RegisterSD(self, request: RA_pb2.RegSDReq, context: grpc.aio.ServicerContext) -> RA_pb2.RegSDRes:
        logging.debug("Got Register SD :")
        logging.debug(request)
        _K_G_SD = await RA().registerSD(ID_SD=request.ID, PID_SD=request.PID, r_SD=request.r)
        response = RA_pb2.RegSDRes(K_G=_K_G_SD.h)
        return response

    async def RegisterMU(self, request: RA_pb2.RegMUReq, context: grpc.aio.ServicerContext) -> RA_pb2.RegMURes:
        logging.debug("Got Register SD :")
        logging.debug(request)
        _K_G_MU, _RID_MU = await RA().registerMU(ID_MU=request.ID, PID_MU=request.PID)
        response = RA_pb2.RegMURes(K_G=_K_G_MU.h, RID=_RID_MU.h)
        return response
