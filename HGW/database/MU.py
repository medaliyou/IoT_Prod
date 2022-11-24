
from database.database import MU_collection
from bson.objectid import ObjectId


# helpers
def MU_helper(MU) -> dict:
    return {
        "id": str(MU["_id"]),
        "ID": MU["ID"],
        "K_G": MU["K_G"],
        "PID": MU["PID"],
        "RID": MU["RID"],
        "PID_n": MU["PID_n"],
        "RID_n": MU["RID_n"]
    }


# Retrieve all MU present in the database
async def retrieve_MUs():
    _MU = []
    async for MU in MU_collection.find():
        _MU.append(MU_helper(MU))
    return _MU


# Add a new MU into to the database
async def add_MU(MU_data: dict) -> dict:
    _MU = await MU_collection.insert_one(MU_data)
    _new_MU = await MU_collection.find_one({"_id": _MU.inserted_id})
    return MU_helper(_new_MU)


# Retrieve a MU with a matching ID
async def retrieve_MU(id: str) -> dict:
    _MU = await MU_collection.find_one({"_id": ObjectId(id)})
    if _MU:
        return MU_helper(_MU)


# Retrieve a MU with a matching PID_MU
async def retrieve_MU_by_PID(PID_MU: str) -> dict:
    _MU = await MU_collection.find_one({"PID": PID_MU})
    if _MU:
        return MU_helper(_MU)


# Retrieve a MU with a matching ID_MU
async def retrieve_MU_by_ID(ID_MU: str) -> dict:
    _MU = await MU_collection.find_one({"ID": ID_MU})
    if _MU:
        return MU_helper(_MU)


# Update a MU with a matching ID
async def update_MU(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    _MU = await MU_collection.find_one({"_id": ObjectId(id)})
    if _MU:
        updated_MU = await MU_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_MU:
            return True
        return False


# Delete a MU from the database
async def delete_MU(id: str):
    _MU = await MU_collection.find_one({"_id": ObjectId(id)})
    if _MU:
        await MU_collection.delete_one({"_id": ObjectId(id)})
        return True