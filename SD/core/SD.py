import asyncio
import logging
import time

from common.Defines import S_RANDOM_NUMBER
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

    def __generate_r(self):
        self.r_SD = X(s=S_RANDOM_NUMBER)  # 128 bits Random Number

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
        self.B1 = self.r_SD ^ (XOps.hash(self.ID_SD + self.K_G_SD))
        # B2 = KGSD ⊕ h(rSD ||KSD )
        self.B2 = self.K_G_SD ^ XOps.hash(self.r_SD + self.K_G_SD)
        # Stores { B1 , B2 , PIDSD } in the memory
        self.registration_state = {
            "B1": self.B1.h,
            "B2": self.B2.h,
            "PID": self.PID_SD.h
        }
        logger.warning(self.registration_state)


async def main(SD_Instance: SD):
    await SD_Instance.init_phase()
    await asyncio.sleep(0.001)
    await SD_Instance.register_phase()
    # asyncio.sleep(0.5)


if __name__ == '__main__':
    SD = SD()
    asyncio.run(main(SD))
