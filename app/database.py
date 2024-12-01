import motor.motor_asyncio
from dotenv import load_dotenv
import os
import logging


# Load environment variables from .env file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()


# MongoDB URI with password correctly encoded
URI = os.environ['MONGO_URI']
client = motor.motor_asyncio.AsyncIOMotorClient(URI)

# Initialize MongoDB client and database
async def check_connection():
    try:
        await client.admin.command("ping")
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error("Could not connect to MongoDB: %s", str(e))
database = client.Students
student_collection = database.get_collection("student_detail")
