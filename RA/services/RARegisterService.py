import asyncio

import grpc

from core.RA import RA
from generated import RA_pb2_grpc, RA_pb2
from common.base_logger import logger
from stubs.HGW import HGW_Client, cHGWClient


class RARegisterService(RA_pb2_grpc.RARegisterServicer):

    async def RegisterSD(self, request: RA_pb2.RegSDReq, context: grpc.aio.ServicerContext) -> RA_pb2.RegSDRes:
        _HGW_Client = await cHGWClient()
        try:
            _K_G_SD = RA().registerSD(ID=request.ID, PID=request.PID, r=request.r)
            # Save it to HGW
            _response = await _HGW_Client.StoreSD(ID=request.ID, PID=request.PID, r=request.r, K_G=_K_G_SD.h)
            logger.info("_response : {}".format(_response))

            if _response is not None:
                logger.info("registerSD : {}".format(_response.status))
                return RA_pb2.RegSDRes(K_G=_K_G_SD.h)
            else:
                logger.warning("StoreSD Failure")

        except Exception as e:
            logger.error(e)

    async def RegisterMU(self, request: RA_pb2.RegMUReq, context: grpc.aio.ServicerContext) -> RA_pb2.RegMURes:
        _HGW_Client = await cHGWClient()
        _K_G_MU, _RID_MU = RA().registerMU(ID=request.ID, PID=request.PID)
        try:
            # Save it to HGW
            _response = await _HGW_Client.StoreMU(ID=request.ID, PID=request.PID, RID=_RID_MU.h, K_G=_K_G_MU.h)
            if _response is not None:
                logger.info("registerMU : {}".format(_response.status))
                return RA_pb2.RegMURes(K_G=_K_G_MU.h, RID=_RID_MU.h)
            else:
                logger.warning("StoreMU Empty _response: _HGW_Client={}".format(_HGW_Client))

        except Exception as e:
            logger.error("Error occurred on RegisterMU")
            logger.error(e)
