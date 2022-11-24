import asyncio
import hashlib
import logging
import time

from common.Defines import *
from common.X import X, XOps
from common.base_logger import logger
from stubs.RA import RA_Client, cRAClient


class MU:
    def __init__(self):

        self.RN_MU: X = None
        self.r_MU: X = None
        self.PID_MU: X = None
        self.RID_MU: X = None
        self.ID_MU: X = None
        self.K_G_MU: X = None
        self.HPW_MU: X = None
        self.PW_MU: X = None

        self.A4: X = None
        self.A3: X = None
        self.A2: X = None
        self.A1: X = None

    def __generate_r(self):
        self.r_MU = X(s=S_RANDOM_NUMBER)  # 128 bits Random Number

    def __compute_PID(self):
        """
        Computes PID MU = h( ID MU ||r MU )
        :return:
        """
        self.PID_MU = XOps.hash(self.ID_MU + self.r_MU)

    async def init_phase(self, ID_MU, PW_MU):
        # _RA_Client = await cRAClient()
        # response = await _RA_Client.GetID()
        # if response is not None:
        hf = hashlib.sha256(ID_MU.encode("UTF-8"))
        _ID_MU = hf.hexdigest()[:S_ID]
        hf = hashlib.sha256(PW_MU.encode("UTF-8"))
        _PW_MU = hf.hexdigest()[:S_PASSWORD]
        self.ID_MU = X(h=_ID_MU)
        self.PW_MU = X(h=_PW_MU)

        self.__generate_r()
        self.__compute_PID()
        logger.info("ID_MU={}".format(self.ID_MU.h))

    async def register_phase(self):
        _RA_Client = await cRAClient()
        response = await _RA_Client.RegisterMU(self.ID_MU.h, self.PID_MU.h)
        if response is not None:
            self.K_G_MU = X(h=response.K_G)
            self.RID_MU = X(h=response.RID)

            logger.info("RID_MU={}".format(self.RID_MU.h))
            logger.info("K_G_MU={}".format(self.K_G_MU.h))
            self.process_register_phase()


    def process_register_phase(self):
        # HPWMU = h( PWMU ||r MU )
        self.HPW_MU = XOps.hash(self.PW_MU + self.r_MU)

        # A1 = r MU ⊕ h( ID MU || PWMU )
        self.A1 = self.r_MU ^ XOps.hash(self.ID_MU + self.ID_MU)

        # A2 = h( ID MU || PWMU ||r MU || HPWMU )
        self.A2 = XOps.hash(self.ID_MU + self.ID_MU + self.r_MU + self.HPW_MU)

        # A3 = RID MU ⊕ h(r MU || HPWMU )
        self.A3 = self.RID_MU ^ XOps.hash(self.r_MU + self.HPW_MU)

        # A4 = K MUG ⊕ h( RID MU || HPWMU )
        self.A4 = self.K_G_MU ^ XOps.hash(self.RID_MU + self.HPW_MU)

        # Stores { A1 , A2 , A3 , A4 , PID MU } in the mobile device
        self.registration_state = {
            "A1": self.A1.h,
            "A2": self.A2.h,
            "A3": self.A3.h,
            "A4": self.A4.h,
            "PID": self.PID_MU.h
        }

        logger.warning(self.registration_state)


async def main(MU_Instance: MU):
    # while 1:
    await MU_Instance.init_phase("username", "password")
    await asyncio.sleep(0.001)
    await MU_Instance.register_phase()
        # asyncio.sleep(0.5)


if __name__ == '__main__':
    MU = MU()
    asyncio.run(main(MU))
