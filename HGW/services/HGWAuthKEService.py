import grpc

from core.HGW import HGW
from generated import HGW_pb2_grpc, HGW_pb2
from database.MU import (
    add_MU, retrieve_MU_by_PID,
)
from database.SD import (
    add_SD,
    retrieve_SD_by_PID
)

from common.base_logger import logger


class HGWAuthKEService(HGW_pb2_grpc.HGWAuthKEServicer):

    async def AuthKES1(self, request: HGW_pb2.AuthKES1Req, context: grpc.aio.ServicerContext) -> HGW_pb2.AuthKES4Res:
        try:
            # search for existing MU with same PID
            _MU = await retrieve_MU_by_PID(request.PID)
            logger.warning("existing_SD = {}".format(_MU))
            if _MU is not None:
                _MU_Auth = {
                    "M1": request.M1,
                    "V": request.V,
                    "C1": request.C1
                }
                await HGW().process_auth_KE_S2(_MU, _MU_Auth)
            else:
                logger.warning("Couldn't find corresponding MU PID={}".format(request.PID))
        except Exception as e:
            logger.error(e)

    async def AuthKES5(self, request: HGW_pb2.AuthKES6Req, context: grpc.aio.ServicerContext) -> HGW_pb2.AuthKES6Res:
        try:
            # search for existing MU with same ID
            existing_MU = await retrieve_MU_by_PID(request.PID)
            logger.warning("existing_MU = {}".format(existing_MU))
            if existing_MU is not None:
                return HGW_pb2.StoreMURes(status="EXISTING")
            else:
                _MU = {
                    "ID": request.ID,
                    "PID": request.PID,
                    "RID": request.RID,
                    "K_G": request.K_G,
                    "PID_n": None,
                    "RID_n": None
                }

                new_MU = await add_MU(_MU)
                if new_MU:
                    logger.info("Added MU successfully ID_MU={}".format(request.ID))
                    return HGW_pb2.StoreMURes(status="OK")
                else:
                    return HGW_pb2.StoreMURes(status="ERROR")
        except Exception as e:
            logger.error(e)
            return HGW_pb2.StoreMURes(status="ERROR")
