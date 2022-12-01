from bson.objectid import ObjectId

from common.base_logger import logger
from database.database import MU_Obj_Collection


def MU_helper(MU) -> dict:
    keys = ["_id"]
    return {k: v for k, v in MU.items() if k not in keys}




# Retrieve all MU present in the database
async def retrieve_MUs():
    _MU = []
    async for mu in MU_Obj_Collection.find():
        _MU.append(MU_helper(mu))
    return _MU


# Add a new MU into to the database
async def add_MU(MU_data: dict) -> dict:
    _MU = await MU_Obj_Collection.insert_one(MU_data)
    _new_MU = await MU_Obj_Collection.find_one({"_id": _MU.inserted_id})
    return MU_helper(_new_MU)


# Retrieve a MU with a matching ID
async def retrieve_MU(id: str) -> dict:
    _MU = await MU_Obj_Collection.find_one({"_id": ObjectId(id)})
    if _MU:
        return MU_helper(_MU)


# Retrieve a MU with a matching PID_MU
async def retrieve_MU_by_PID(PID_MU: str) -> dict:
    _MU = await MU_Obj_Collection.find_one({"PID_MU": PID_MU})
    if _MU:
        return MU_helper(_MU)


# Retrieve a MU with a matching TAG_MU
async def retrieve_MU_by_TAG(TAG) -> dict:
    print("TAG_MU", TAG)
    _MU = await MU_Obj_Collection.find_one({"TAG_MU": TAG})
    if _MU:
        return MU_helper(_MU)


# Retrieve a MU with a matching ID_MU
async def retrieve_MU_by_ID(ID_MU: str) -> dict:
    _MU = await MU_Obj_Collection.find_one({"ID_MU": ID_MU})
    if _MU:
        return MU_helper(_MU)


# Update a MU with a matching ID
async def update_MU(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    _MU = await MU_Obj_Collection.find_one({"_id": ObjectId(id)})
    if _MU:
        updated_MU = await MU_Obj_Collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_MU:
            return True
        return False


# Update a MU with a matching PID
async def update_MU_by_PID(PID: str, data: dict):
    # Return false if an empty request body is sent.
    _MU = await MU_Obj_Collection.find_one({"PID_MU": PID})
    logger.warning("Retrieved MU")
    logger.warning(_MU)

    if _MU:
        updated_MU = await MU_Obj_Collection.update_one(
            {"PID_MU": PID}, {"$set": data}

        )
        logger.warning("updated_MU")

        logger.warning(updated_MU)

        if updated_MU:
            return True
        return False


# Delete a MU from the database
async def delete_MU(id: str):
    _MU = await MU_Obj_Collection.find_one({"_id": ObjectId(id)})
    if _MU:
        await MU_Obj_Collection.delete_one({"_id": ObjectId(id)})
        return True

