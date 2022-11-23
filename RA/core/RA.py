import grpc

from common.SingletonMeta import SingletonMeta
from common.X import X, XOps
from common.base_logger import logger

from stubs.HGW import HGWClient


class RA(metaclass=SingletonMeta):

    def __init__(self):
        self.K_RA = None
        self.r_RA = None

        self.__generate_K_RA()
        self.__generate_r_RA()

        self._HGW_Client = HGWClient()

    def __generate_K_RA(self):
        # Generate Random K{RA} - 128 bits
        if self.K_RA is None:
            self.K_RA = X(s=X.S_KEY)  # 16 bytes

    def __generate_r_RA(self):
        # Generate Random r{RA} - 128 bits
        if self.r_RA is None:
            self.r_RA = X(s=X.S_RANDOM_NUMBER)  # 16 bytes

    def __compute_K_G_SD(self, PID_SD):
        assert isinstance(PID_SD, X)
        # Computes
        # KGSD = h( PIDSD ||K RA ||r RA )
        return XOps.hash(PID_SD + self.K_RA + self.r_RA)

    def __compute_K_G_MU(self, PID_MU):
        assert isinstance(PID_MU, X)
        # Computes
        # K MUG = h( PID MU ||K RA ||r RA )
        return XOps.hash(PID_MU + self.K_RA + self.r_RA)

    def __compute_RID_MU(self, PID_MU, K_G_MU):
        assert isinstance(PID_MU, X)
        assert isinstance(K_G_MU, X)
        # RID MU = h( PID MU || K MUG )
        return XOps.hash(PID_MU + K_G_MU)

    async def registerSD(self, ID_SD, PID_SD, r_SD) -> X:
        _PID_SD = X(h=PID_SD)
        _r_SD = X(h=r_SD)
        _ID_SD = X(h=ID_SD)
        _K_G_SD = self.__compute_K_G_SD(_PID_SD)
        logger.info("K_G_SD={}".format(_K_G_SD))
        # Save it to HGW
        response = await self._HGW_Client.StoreSD(_ID_SD.h, _PID_SD.h, _r_SD.h, _K_G_SD.h)
        logger.info("registerSD : {}".format(response.status))
        return _K_G_SD

    async def registerMU(self, ID_MU, PID_MU) -> (X, X):
        _PID_MU = X(h=PID_MU)
        _ID_MU = X(h=ID_MU)
        _K_G_MU = self.__compute_K_G_MU(_PID_MU)
        _RID_MU = self.__compute_RID_MU(_PID_MU, _K_G_MU)
        logger.info("K_G_MU={}".format(_K_G_MU))
        logger.info("RID_MU={}".format(_RID_MU))
        # Save it to HGW
        response = await self._HGW_Client.StoreMU(_ID_MU.h, _PID_MU.h, _RID_MU.h, _K_G_MU.h)
        logger.info("registerMU : {}".format(response.status))
        return _K_G_MU, _RID_MU


