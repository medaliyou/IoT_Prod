from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from common.base_logger import logger
from core.MU import MU, parse_credentials
from database.MU_Obj import (
    add_MU,
    retrieve_MUs,
    retrieve_MU_by_PID,
    retrieve_MU_by_TAG, retrieve_MU_by_ID
)

router = APIRouter()


@router.get("/", tags=["GetMUs"])
async def GetMUs():
    _MUs = await retrieve_MUs()
    logger.info(_MUs)
    return {"data": _MUs}


class Register(BaseModel):
    TAG: str
    ID: str
    PW: str


@router.post("/", tags=["CreateMU"])
async def CreateMU(reg: Register):
    # Make sure this ID is unique
    _ID_MU, _PW_MU = parse_credentials(reg.ID, reg.PW)

    _existing_MU = await retrieve_MU_by_ID(_ID_MU.h)
    if _existing_MU is not None:
        raise HTTPException(
            status_code=409,  # 409 Conflict
            detail="ID is already registered",
            headers={"X-Error": "ID exists"},
        )

    _MU = MU(reg.TAG)
    await _MU.init_phase(reg.ID, reg.PW)
    await _MU.register_phase()
    logger.info(_MU.export_dict())

    _saved_MU = await add_MU(_MU.export_dict())
    return _saved_MU


@router.get("/PID/{PID}", tags=["LoadMU"])
async def LoadMU(PID: str):
    logger.info(PID)
    if PID is not None:
        _saved_MU = await retrieve_MU_by_PID(PID)
    logger.info(_saved_MU)

    if _saved_MU is None:
        return {}
    _MU = MU()
    _MU.import_dict(_saved_MU)
    logger.info(_saved_MU)
    logger.info(_MU)

    return _saved_MU


@router.get("/TAG/{TAG}", tags=["LoadMU"])
async def LoadMU(TAG: str):
    logger.info(TAG)
    if TAG is not None:
        _saved_MU = await retrieve_MU_by_TAG(TAG)
    logger.info(_saved_MU)

    if _saved_MU is None:
        return {}
    _MU = MU()
    _MU.import_dict(_saved_MU)
    logger.info(_saved_MU)
    logger.info(_MU)

    return _saved_MU
