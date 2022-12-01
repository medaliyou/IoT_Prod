import grpc

from core.context import SD_Context
from generated import SD_pb2, SD_pb2_grpc

from common.base_logger import logger


class SDAuthKEService(SD_pb2_grpc.SDAuthKEServicer):

    async def AuthKES3(self, request: SD_pb2.AuthKES3Req, context: grpc.aio.ServicerContext) -> SD_pb2.AuthKES3Res:
        try:



            # search for existing MU with same PID
            _PID_MU = request.PID
            _M3 = request.M3
            _C2 = request.C2
            _V_G_MU = request.V
            logger.info(request)
            assert SD_Context.ctx is not None
            _M4, _V_MU = await SD_Context.ctx.process_auth_KE_S3(PID=_PID_MU, M3=_M3, C2=_C2, V=_V_G_MU)
            return SD_pb2.AuthKES3Res(M4=_M4.h, V=_V_MU.h)
        except Exception as e:
            logger.error(e)
