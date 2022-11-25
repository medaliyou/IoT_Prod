from common.Defines import S_ID, S_RANDOM_NUMBER
from common.SingletonMeta import SingletonMeta
from common.X import X, XOps
from common.base_logger import logger
from database.SD import retrieve_SD_by_PID
from stubs.SD import cSDClient


class HGW(metaclass=SingletonMeta):

    def __init__(self):
        pass

    def __generate_RN(self):
        self.RN = X(s=S_RANDOM_NUMBER)

    async def __get_corresponding_SD(self, PID):
        _SD = await retrieve_SD_by_PID(PID)
        logger.debug("Retrieving SD")
        logger.debug(_SD)
        return _SD

    async def process_auth_KE_S2(self, MU, MU_Auth):
        try:
            # Retrieves RID MU and K MUG corresponding to PID MU
            _ID_MU = X(h=MU["ID"])
            _PID_MU = X(h=MU["PID"])
            _K_G_MU = X(h=MU["K_G"])
            _RID_MU = X(h=MU["RID"])
            _M1 = X(h=MU_Auth["M1"])
            _V = X(h=MU_Auth["V"])
            _C1 = X(h=MU_Auth["C1"])

            # ( RN*MU || PID∗SD ) = M1 ⊕ h ( PID MU || RID MU || K MUG )
            # __concat_RN_MU_star_PID_SD_star
            _c_RNMU_star_PIDSD_star = _M1 ^ XOps.hash(_PID_MU + _RID_MU + _K_G_MU)

            len_concat = len(_c_RNMU_star_PIDSD_star.b)
            # Make sure l % 2 == 0
            assert len_concat & 1 == 0
            _RN_MU_star = X(b=_c_RNMU_star_PIDSD_star.b[:S_ID])  # 16 bytes sizeof (RN_MU)
            _PID_SD_star = X(b=_c_RNMU_star_PIDSD_star.b[S_ID:])

            # V*MU = h ( PID MU || RID MU || RN*MU || PID*SD || K MUG )
            _V_MU_star = XOps.hash(_PID_MU + _RID_MU + _c_RNMU_star_PIDSD_star + _K_G_MU)

            # Checks V_MU∗ = V_MU
            logger.warning(
                "Checks V_MU∗ == V_MU"
            )
            logger.warning(
                "V_MU∗ = {}".format(_V_MU_star)
            )
            logger.warning(
                "V_MU = {}".format(_V)
            )

            if _V_MU_star != _V:
                return

            # Retrieves KGSD and rSD corresponding to PIDSD
            _SD = await self.__get_corresponding_SD(_PID_SD_star.h)

            assert _SD is not None
            _PID_SD = X(h=_SD["PID"])
            _K_G_SD = X(h=_SD["K_G"])
            _r_SD = X(h=_SD["r"])

            # Generates RNG
            self.__generate_RN()

            # Computes
            # M2 = h( RNMU || RNG )
            _M2 = XOps.hash(_RN_MU_star + self.RN)

            # M3 = h( PIDSD ||KGSD ||rSD ) ⊕ M2
            _M3 = XOps.hash(_PID_SD + _K_G_SD + _r_SD) ^ _M2

            # h( ID MU || RNMU ) = C1 ⊕ h(K MUG || RNMU )
            _hash_IDMU_RNMU = _C1 ^ XOps.hash(_K_G_MU + _RN_MU_star)

            # C2 = (h( ID MU || RNMU )||h( IDG || RNG )) ⊕ h(KGSD ||rSD )
            _C2 = (_hash_IDMU_RNMU + XOps.hash(self.ID_HGW + self.RN) + XOps.hash(_K_G_SD + _r_SD))

            # VMUG = h( PID MU || M2 ||KGSD )
            _V_G_MU = XOps.hash(_PID_MU + _M2 + _K_G_SD)

            '''
                Save the Objects context from the first Request
            '''
            # Update S2
            self.S2 = {
                "ID_MU": _ID_MU,
                "PID_MU": _PID_MU,
                "K_G_MU": _K_G_MU,
                "RID_MU": _RID_MU,
                "RN_MU": _RN_MU_star,
                "M2": _M2,
                "M3": _M3,
                "C2": _C2,
                "V_G": _V_G_MU

            }

            self.auth_KE_S2_state = {
                "PID": _PID_MU.h,
                "M3": _M3.h,
                "C2": _C2.h,
                "V_G": _V_G_MU.h
            }
            _SD_Client = await cSDClient()

            response = await _SD_Client.AuthKES3(PID_MU=_PID_MU.h, C2=_C2.h, M3=_M3.h, V_G_MU=_V_G_MU.h)
            if response is not None:
                logger.warning(response)

        except Exception as e:
            logger.error(e)
