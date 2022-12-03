from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from common.base_logger import logger
from core.context import SD_Context, Context
from core.SD import SD
from database.SD_Obj import (
    add_SD,
    retrieve_SDs,
    retrieve_SD_by_PID,
    retrieve_SD_by_TAG,
    delete_SDs,
    delete_SD_by_PID
)

router = APIRouter()


@router.get("/", tags=["GetSDs"])
async def GetSDs():
    _SDs = await retrieve_SDs()
    logger.info(_SDs)
    return {"data": _SDs}


class SmartDevice(BaseModel):
    TAG_SD: str


@router.post("/", tags=["CreateSD"])
async def CreateSD(sd: SmartDevice):
    _existing_SD = await retrieve_SD_by_TAG(sd.TAG_SD)
    if _existing_SD is not None:
        raise HTTPException(
            status_code=409,  # 409 Conflict
            detail="ID is already registered",
            headers={"X-Error": "ID exists"},
        )

    _SD = SD(sd.TAG_SD)
    await _SD.init_phase()
    await _SD.register_phase()
    logger.info(_SD.export_dict())
    _saved_SD = await add_SD(_SD.export_dict())
    # Set SD_context object
    Context().ctx = _SD

    logger.info(Context().ctx.TAG_SD)
    logger.info(Context().ctx.PID_SD)

    return _saved_SD


@router.get("/PID/{PID}", tags=["LoadSD"])
async def LoadSD(PID: str):
    logger.info(PID)
    if PID is not None:
        _saved_SD = await retrieve_SD_by_PID(PID)
    logger.info(_saved_SD)

    if _saved_SD is None:
        return {}
    _SD = SD()
    _SD.import_dict(_saved_SD)

    logger.info(_saved_SD)
    logger.info(_SD)
    # Set SD_context object
    Context().ctx = _SD

    logger.info(Context().ctx.TAG_SD)
    logger.info(Context().ctx.PID_SD)

    return _saved_SD


@router.get("/TAG/{TAG}", tags=["LoadSD"])
async def LoadSD(TAG: str):
    logger.info(TAG)
    if TAG is not None:
        _saved_SD = await retrieve_SD_by_TAG(TAG)
    logger.info(_saved_SD)

    if _saved_SD is None:
        return {}
    _SD = SD()
    _SD.import_dict(_saved_SD)

    logger.info(_saved_SD)
    logger.info(_SD)
    # Set SD_context object
    Context().ctx = _SD

    logger.info(Context().ctx.TAG_SD)
    logger.info(Context().ctx.PID_SD)

    return _saved_SD


@router.delete("/PID/{pid}", tags=["DeleteSD"])
async def deleteSD_by_PID(pid: str):
    result = await delete_SD_by_PID(pid)
    logger.info("Deleting SD PID={}, RESULT={}".format(pid, result))
    return result


@router.delete("/All", tags=["DeleteSDs"])
async def deleteAllSDs():
    logger.info("Deleting All SDs")
    deleted_count = await delete_SDs()
    logger.info(deleted_count)
    return deleted_count
