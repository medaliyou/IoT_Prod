from bson.objectid import ObjectId

from common.base_logger import logger
from database.database import SD_Obj_Collection


# helpers
# def SD_helper(SD) -> dict:
#     return {
#         "id": str(SD["_id"]),
#         "ID": SD["ID"],
#         "K_G": SD["K_G"],
#         "PID": SD["PID"],
#         "r": SD["r"],
#      }

def SD_helper(SD) -> dict:
    keys = ["_id"]
    return {k: v for k, v in SD.items() if k not in keys}


# # Retrieve all SD present in the database
# async def retrieve_SDs():
#     _SD = []
#     async for sd in SD_Obj_Collection.find():
#         _SD.append(SD_helper(sd))
#     return _SD
# Retrieve all SD present in the database
async def retrieve_SDs():
    _SD = []
    async for sd in SD_Obj_Collection.find():
        _SD.append(SD_helper(sd))
    return _SD


# Add a new SD into to the database
async def add_SD(SD_data: dict) -> dict:
    _SD = await SD_Obj_Collection.insert_one(SD_data)
    _new_SD = await SD_Obj_Collection.find_one({"_id": _SD.inserted_id})
    return SD_helper(_new_SD)


# Retrieve a SD with a matching ID
async def retrieve_SD(id: str) -> dict:
    _SD = await SD_Obj_Collection.find_one({"_id": ObjectId(id)})
    if _SD:
        return SD_helper(_SD)


# Retrieve a SD with a matching PID_SD
async def retrieve_SD_by_PID(PID_SD: str) -> dict:
    _SD = await SD_Obj_Collection.find_one({"PID_SD": PID_SD})
    if _SD:
        return SD_helper(_SD)


# Retrieve a SD with a matching TAG_SD
async def retrieve_SD_by_TAG(TAG) -> dict:
    print("TAG_SD", TAG)
    _SD = await SD_Obj_Collection.find_one({"TAG_SD": TAG})
    if _SD:
        return SD_helper(_SD)


# Retrieve a SD with a matching ID_SD
async def retrieve_SD_by_ID(ID_SD: str) -> dict:
    _SD = await SD_Obj_Collection.find_one({"ID_SD": ID_SD})
    if _SD:
        return SD_helper(_SD)


# Update a SD with a matching ID
async def update_SD(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    _SD = await SD_Obj_Collection.find_one({"_id": ObjectId(id)})
    if _SD:
        updated_SD = await SD_Obj_Collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_SD:
            return True
        return False


# Update a SD with a matching PID
async def update_SD_by_PID(PID: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    _SD = await SD_Obj_Collection.find_one({"PID_SD": PID})
    if _SD:
        updated_SD = await SD_Obj_Collection.update_one(
            {"PID_SD": PID}, {"$set": data}
        )
        if updated_SD:
            return True
        return False


# Delete a SD from the database
async def delete_SD(id: str):
    _SD = await SD_Obj_Collection.find_one({"_id": ObjectId(id)})
    if _SD:
        await SD_Obj_Collection.delete_one({"_id": ObjectId(id)})
        return True
