import motor.motor_asyncio
from config.config import settings

MONGO_DETAILS = settings.DB_URL
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Database
database = client.IoT_Context
# Collections
MU_Obj_Collection = database.get_collection("MU")
