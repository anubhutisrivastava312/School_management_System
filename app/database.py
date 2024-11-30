import motor.motor_asyncio
from dotenv import load_dotenv
import os
import logging
from urllib.parse import quote_plus
# Load environment variables from .env file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
# username = quote_plus(os.getenv("USERNAME"))
# password = quote_plus(os.getenv("PASSWORD"))
# uri = os.getenv("URI")

# MongoDB URI with password correctly encoded
MONGO_URI = "mongodb+srv://anubhutisrivastava312:anubhuti123@cluster0.ftqij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

# Initialize MongoDB client and database
async def check_connection():
    try:
        await client.admin.command("ping")
        logger.info("Successfully connected to MongoDB!")
    except Exception as e:
        logger.error("Could not connect to MongoDB: %s", str(e))

database = client.Students

student_collection = database.get_collection("student_detail")
