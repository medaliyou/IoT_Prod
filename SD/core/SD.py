import asyncio
import logging
import time

from common.Defines import S_RANDOM_NUMBER, S_KEY
from common.X import X, XOps
from common.base_logger import logger
from stubs.RA import RA_Client, cRAClient


class SD:
    def __init__(self):
        self.B1 = None
        self.B2 = None
        self.registration_state = None
        self.r_SD: X = None
        self.RN_SD: X = None
        self.PID_SD: X = None
        self.ID_SD: X = None
        self.K_G_SD: X = None
        self.K_SD: X = None

    def __generate_r(self):
        self.r_SD = X(s=S_RANDOM_NUMBER)  # 128 bits Random Number

    def __generate_K(self):
        self.K_SD = X(s=S_KEY)  # 128 bits Random Number
    def __generate_RN(self):
        self.RN_SD = X(s=S_RANDOM_NUMBER)

    def __compute_PID(self):
        """
        Computes PIDSD = h( IDSD ||rSD )
        :return:
        """
        # __concat = Ops.ops_concatenate(self.ID, self.r)
        self.PID_SD = XOps.hash(self.ID_SD + self.r_SD)

    async def init_phase(self):
        RA_Client = await cRAClient()
        response = await RA_Client.GetID()
        if response is not None:
            self.ID_SD = X(h=response.ID)
            self.__generate_r()
            self.__generate_K()
            self.__compute_PID()
            logger.info("ID_SD={}".format(self.ID_SD.h))

    async def register_phase(self):
        RA_Client = await cRAClient()
        response = await RA_Client.RegisterSD(self.ID_SD.h, self.PID_SD.h, self.r_SD.h)
        if response is not None:
            self.K_G_SD = X(h=response.K_G)
            logger.info("K_G_SD={}".format(self.K_G_SD.h))
            self.process_register_phase()

    def process_register_phase(self):

        # B1 = rSD ⊕ h( IDSD ||KSD )
        self.B1 = self.r_SD ^ (XOps.hash(self.ID_SD + self.K_SD))
        # B2 = KGSD ⊕ h(rSD ||KSD )
        self.B2 = self.K_G_SD ^ XOps.hash(self.r_SD + self.K_SD)
        # Stores { B1 , B2 , PIDSD } in the memory
        self.registration_state = {
            "B1": self.B1.h,
            "B2": self.B2.h,
            "PID": self.PID_SD.h
        }
        logger.warning(self.registration_state)

    async def process_auth_KE_S3(self, PID, M3, C2, V):
        try:
            _PID_MU = X(h=PID)
            _M3 = X(h=M3)
            _C2 = X(h=C2)
            _V_G_MU = X(h=V)

            # Computes
            # rSD = B1 ⊕ h( IDSD ||KSD )
            _r_SD = self.B1 ^ XOps.hash(self.ID_SD + self.K_SD)

            # KGSD = B2 ⊕ h(rSD ||KSD )
            _K_G_SD = self.B2 ^ XOps.hash(_r_SD + self.K_SD)

            # M2∗ = M3 ⊕ h( PIDSD ||KGSD ||rSD )
            _M2_star = _M3 ^ XOps.hash(self.PID_SD + _K_G_SD + _r_SD)
            # VMUG* = h( PID MU || M2∗ ||KGSD )
            _V_G_MU_star = XOps.hash(_PID_MU + _M2_star + _K_G_SD)

            # Checks VMUG* = VMUG

            logger.warning(
                "Checks VMUG* == VMUG"
            )
            logger.warning(
                "VMUG* = {}".format(_V_G_MU_star.h)
            )
            logger.warning(
                "VMUG = {}".format(_V_G_MU)
            )

            if _V_G_MU_star != _V_G_MU:
                # Verification not successful

                return

            # Indicate to Backend that Registration Was OK
            # and continue calculation

            # Generates RNSD
            self.__generate_RN()

            # Computes
            # (h( ID MU || RNMU )||h( IDG || RNG )) = C2 ⊕ h(KGSD ||rSD )
            _hash_IDMU_RNMU_c_hash_IDG_RNG = _C2 ^ XOps.hash(_K_G_SD + _r_SD)

            # SK = h( h( ID MU || RNMU )||h( IDG || RNG ) || h( IDSD || RNSD ))
            self.SK = XOps.hash(
                _hash_IDMU_RNMU_c_hash_IDG_RNG + XOps.hash(self.ID_SD + self.RN_SD)
            )
            logger.warning("\n[SESSION KEY]={}".format(self.SK))

            # M4 = h( PIDSD ||KGSD ||rSD ) ⊕ h( IDSD || RNSD )
            _M4 = XOps.hash(self.PID_SD + _K_G_SD + _r_SD) ^ XOps.hash(self.ID_SD + self.RN_SD)

            # VSD = h( PID MU || PIDSD || M2∗ ||h( IDSD || RNSD )||KGSD )
            _V_SD = XOps.hash(_PID_MU + self.PID_SD + _M2_star + XOps.hash(self.ID_SD + self.RN_SD) + _K_G_SD)


            self.authentication_state = {
                "M4": _M4,
                "V": _V_SD,
                "PID": self.PID_SD
            }
            return _M4, _V_SD


        except Exception as e:
            logger.error(e)


async def main(SD_Instance: SD):
    await SD_Instance.init_phase()
    await asyncio.sleep(0.001)
    await SD_Instance.register_phase()
    # asyncio.sleep(0.5)


if __name__ == '__main__':
    SD = SD()
    asyncio.run(main(SD))
