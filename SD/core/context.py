from common.SingletonMeta import SingletonMeta
from common.X import X
from common.base_logger import logger
from core.SD import SD

from database.SD_Obj import (update_SD_by_PID)


class Context(object, metaclass=SingletonMeta):
    ctx: SD = None

    def __init__(self):
        logger.warning("Context __init__()")

    @staticmethod
    async def save(SD_Object: SD):
        logger.info("Context Saving SD Object")
        logger.info(SD_Object)
        try:
            _dict = SD_Object.export_dict()
            result = await update_SD_by_PID(SD_Object.PID_SD, _dict)
            return result
        except Exception as e:
            logger.error(e)


SD_Context = Context()

if __name__ == '__main__':
    print(Context().ctx)
    print(SD_Context.ctx)
