import motor.motor_asyncio
from config.config import settings

MONGO_DETAILS = settings.DB_URL
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Database
database = client.IoT
# Collections
SD_collection = database.get_collection("SD_collection")
MU_collection = database.get_collection("MU_collection")