import grpc

from common.SingletonMeta import SingletonMeta
from common.X import X, XOps
from common.base_logger import logger


class RA(metaclass=SingletonMeta):

    def __init__(self):
        self.K_RA = None
        self.r_RA = None

        self.__generate_K_RA()
        self.__generate_r_RA()

    def __generate_K_RA(self):
        # Generate Random K{RA} - 128 bits
        if self.K_RA is None:
            self.K_RA = X(s=X.S_KEY)  # 16 bytes

    def __generate_r_RA(self):
        # Generate Random r{RA} - 128 bits
        if self.r_RA is None:
            self.r_RA = X(s=X.S_RANDOM_NUMBER)  # 16 bytes

    def __compute_K_G_MU(self, PID_MU):
        assert isinstance(PID_MU, X)
        # Computes
        # KGSD = h( PIDSD ||K RA ||r RA )
        return XOps.hash(PID_MU + self.K_RA + self.r_RA)

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

    def registerSD(self, ID, PID, r) -> X:
        _PID_MU = X(h=PID)
        _r_MU = X(h=r)
        _ID_MU = X(h=ID)
        _K_G_MU = self.__compute_K_G_MU(_PID_MU)
        logger.info("K_G_MU={}".format(_K_G_MU))
        return _K_G_MU

    def registerMU(self, ID, PID) -> (X, X):
        _PID_MU = X(h=PID)
        _ID_MU = X(h=ID)
        _K_G_MU = self.__compute_K_G_MU(_PID_MU)
        _RID_MU = self.__compute_RID_MU(_PID_MU, _K_G_MU)
        logger.info("K_G_MU={}".format(_K_G_MU))
        logger.info("RID_MU={}".format(_RID_MU))
        return _K_G_MU, _RID_MU


