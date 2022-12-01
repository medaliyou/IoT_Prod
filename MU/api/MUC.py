import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from common.Defines import ErrorModel
from common.base_logger import logger
from config.config import settings
from core.MU import MU, parse_credentials
from database.MU_Obj import (
    add_MU,
    retrieve_MUs,
    retrieve_MU_by_PID,
    retrieve_MU_by_TAG, retrieve_MU_by_ID
)

router = APIRouter()


class Credentials(BaseModel):
    ID: str
    PW: str


MU_Ctx: MU = None


@router.post("/login", tags=["login"])
async def login(c: Credentials):
    global MU_Ctx
    logger.info(c.ID)
    logger.info(c.PW)
    _ID, _PW = parse_credentials(c.ID, c.PW)
    _existing_MU = await retrieve_MU_by_ID(_ID.h)

    if _existing_MU is None:
        raise HTTPException(
            status_code=404,  # 404 - Conflict
            detail="ID is not registered",
            headers={"X-Error": "ID does not exist"},
        )
    if _existing_MU['PW_MU'] != _PW.h:
        raise HTTPException(
            status_code=403,  # 403 - Forbidden
            detail="Incorrect password",
            headers={"X-Error": "Password is incorrect"},
        )

    _MU = MU()
    _MU.import_dict(_existing_MU)

    # logger.warning(_MU)
    # logger.warning(_MU.PW_MU)
    # logger.warning(type(_MU.PW_MU))
    #
    # logger.warning(_MU.PID_MU)
    # logger.warning(type(_MU.PID_MU))

    # Set MU Context to logged in MU
    MU_Ctx = _MU

    return _existing_MU


@router.post("/logout", tags=["logout"])
async def logout():
    global MU_Ctx
    if MU_Ctx is None:
        raise HTTPException(
            status_code=404,  # 404 - Conflict
            detail="Already logged out",
            headers={"X-Error": "You are not logged in"},
        )
    else:
        MU_Ctx = None
        return None


@router.post("/auth", tags=["auth"])
async def auth(PID_SD):
    global MU_Ctx
    if MU_Ctx is None:
        raise HTTPException(
            status_code=403,  # 403 - Authorized
            detail="Not Authorized! Are you Logged in ?",
            headers={"X-Error": "Not Authorized"},
        )
    # Try to Load designated SD object
    response = await load_SD(PID_SD)
    if response.err_no != 0:
        raise HTTPException(
            status_code=501,  # 501 - Authorized
            detail=response.err_message,
        )

    logger.info(PID_SD)
    logger.info(MU_Ctx.ID_MU)
    logger.info(MU_Ctx.PW_MU)
    response: ErrorModel = await MU_Ctx.auth_KE_phase(MU_Ctx.ID_MU.h, MU_Ctx.PW_MU.h, PID_SD)
    if response.err_no != 0:
        raise HTTPException(
            status_code=501,  # 501 - Authorized
            detail=response.err_message,

        )
    else:
        return response


async def load_SD(PID_SD: str):
    request_url = "http://{}:{}/SD/PID/{}".format(settings.SD_H, settings.SD_API_PORT, PID_SD)
    try:
        response = requests.get(request_url)
        if response is not None:
            logger.warning(response)
            return ErrorModel(0, response)
    except Exception as e:
        logger.error(e)
        return ErrorModel(1, response)

