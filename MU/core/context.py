from common.base_logger import logger
from database.MU_Obj import (update_MU_by_PID)


async def save(MU_Object):
    logger.info("Context Saving MU Object")
    logger.info(MU_Object)
    try:
        _dict = MU_Object.export_dict()
        print("*"*100)
        print("save")
        print("*"*100)

        print(_dict)
        print("*"*100)

        result = await update_MU_by_PID(MU_Object.PID_MU_old, _dict)
        return result
    except Exception as e:
        logger.error(e)

