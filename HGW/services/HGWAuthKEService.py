import grpc

from common.Defines import ErrorModel
from common.X import X
from core.HGW import HGW
from generated import HGW_pb2_grpc, HGW_pb2
from database.MU import (
    add_MU, retrieve_MU_by_PID,
)

from common.base_logger import logger


class HGWAuthKEService(HGW_pb2_grpc.HGWAuthKEServicer):

    async def AuthKES1(self, request: HGW_pb2.AuthKES1Req, context: grpc.aio.ServicerContext) -> HGW_pb2.AuthKES4Res:
        try:
            # search for existing MU with same PID
            _MU = await retrieve_MU_by_PID(request.PID)
            logger.warning("existing_MU = {}".format(_MU))
            if _MU is not None:
                _MU_Auth = {
                    "M1": request.M1,
                    "V": request.V,
                    "C1": request.C1
                }
                M5, V_G_SD = await HGW().process_auth_KE(_MU, _MU_Auth)
                logger.info(M5)
                logger.info(V_G_SD)
                return HGW_pb2.AuthKES4Res(M5=M5.h, V_G=V_G_SD.h)

            else:
                logger.warning("Couldn't find corresponding MU PID={}".format(request.PID))
        except Exception as e:
            logger.error(e)

    async def AuthKES6(self, request: HGW_pb2.AuthKES6Req, context: grpc.aio.ServicerContext) -> HGW_pb2.AuthKES6Res:
        try:
            # search for existing MU with same ID
            res = await HGW().process_auth_KE_S6(M6=request.M6, PID_MU=request.PID)
            return HGW_pb2.AuthKES6Res(status=res.err_message)

        except Exception as e:
            logger.error(e)
            return HGW_pb2.AuthKES6Res(status="ERROR")
