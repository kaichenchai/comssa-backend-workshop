import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "")
UNIQUE_URL_ID = os.getenv("UNIQUE_URL_ID", "")

# Construct the URL to our mongodb, obtain the template from MongoDB Atlas portal

MONGODB_URL = f"mongodb+srv://{quote_plus(MONGODB_USERNAME)}:{quote_plus(MONGODB_PASSWORD)}@{quote_plus(CLUSTER_NAME)}.{quote_plus(UNIQUE_URL_ID)}.mongodb.net/?retryWrites=true&w=majority&appName={quote_plus(CLUSTER_NAME)}"


# Create the MongoDB client
client = MongoClient(MONGODB_URL)

# Get the database
database = client[DATABASE_NAME]

# Test the connection (optional but helpful for debugging)
def ping_database():
    try:
        # The ping command is a simple way to test if the database is accessible
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False
