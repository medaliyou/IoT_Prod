import asyncio
import logging

from common.X import X, XOps
from common.base_logger import logger
from stubs.RA import RAClient


class SD:
    def __init__(self):
        self.RA_Client = RAClient()
        self.r_SD: X = None
        self.RN_SD: X = None
        self.PID_SD: X = None
        self.ID_SD: X = None
        self.K_G_SD: X = None

    async def init_channel(self):
        await self.RA_Client.init_channel()

    async def init_phase(self):
        response = await self.RA_Client.GetID()
        self.ID_SD = X(h=response.ID)
        logger.info("ID_SD={}".format(self.ID_SD.h))

    async def register_phase(self):
        response = await self.RA_Client.RegisterSD(self.ID_SD.h)
        self.K_G_SD = X(h=response.K_G)
        logger.info("K_G_SD={}".format(self.K_G_SD.h))


async def main(SD_Instance: SD):
    await SD_Instance.init_channel()
    await SD_Instance.init_phase()
    await SD_Instance.register_phase()


if __name__ == '__main__':
    SD = SD()
    asyncio.run(main(SD))
