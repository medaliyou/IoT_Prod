import grpc
from generated import HGW_pb2_grpc, HGW_pb2
from database.MU import (
    add_MU, retrieve_MU_by_PID,
)
from database.SD import (
    add_SD,
    retrieve_SD_by_PID
)

from common.base_logger import logger


class HGWRegisterService(HGW_pb2_grpc.HGWRegisterServicer):

    async def StoreSD(self, request: HGW_pb2.StoreSDReq, context: grpc.aio.ServicerContext) -> HGW_pb2.StoreSDRes:
        try:
            # search for existing SD with same ID
            existing_SD = await retrieve_SD_by_PID(request.PID)
            logger.warning("existing_SD = {}".format(existing_SD))

            if existing_SD is not None:
                return HGW_pb2.StoreSDRes(status="EXISTING")
            else:
                _SD = {
                    "ID": request.ID,
                    "PID": request.PID,
                    "r": request.r,
                    "K_G": request.K_G
                }

                new_SD = await add_SD(_SD)
                if new_SD:
                    logger.info("Added SD successfully ID_SD={}".format(request.ID))
                    return HGW_pb2.StoreSDRes(status="OK")
                else:
                    return HGW_pb2.StoreSDRes(status="ERROR")
        except Exception as e:
            logger.error(e)
            return HGW_pb2.StoreSDRes(status="ERROR")

    async def StoreMU(self, request: HGW_pb2.StoreMUReq, context: grpc.aio.ServicerContext) -> HGW_pb2.StoreMURes:
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
