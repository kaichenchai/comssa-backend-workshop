from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from pymongo.collection import Collection

from database import database
from models import User, UserCreate, UserUpdate

# Get the users collection - think of this as a table in traditional databases
users_collection: Collection = database.get_collection("users")

def create_user(user: UserCreate) -> User:
    """Create a new user in the database"""
    # Convert the Pydantic model to a dictionary that MongoDB can understand
    user_dict = user.model_dump()

    # Add a timestamp when the user was created
    user_dict["created_at"] = datetime.now(timezone.utc)

    # Insert the user into the database - MongoDB automatically creates an _id
    result = users_collection.insert_one(user_dict)

    # Get the newly created user from the database using the generated ID
    created_user = users_collection.find_one({"_id": result.inserted_id})

    if created_user is None:
        raise ValueError("User creation failed, user not found in database.")

    # MongoDB ObjectIds are not JSON serializable, so convert to string
    created_user["_id"] = str(created_user["_id"])

    # Return the user as a Pydantic model for validation and response
    return User(**created_user)

def get_user_by_id(user_id: str) -> Optional[User]:
    """Get a user by their ID"""
    # First, check if the provided ID is a valid MongoDB ObjectId
    if not ObjectId.is_valid(user_id):
        return None

    # Search for the user in the database using their ID
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    # If we found a user, process and return it
    if user:
        # Convert ObjectId to string for JSON serialization
        user["_id"] = str(user["_id"])
        return User(**user)

    # Return None if no user was found
    return None

def get_all_users() -> List[User]:
    """Get all users from the database"""
    # Create a cursor to iterate through all users
    cursor = users_collection.find()
    users = []

    # Loop through each user document in the database
    for user in cursor:
        # Convert ObjectId to string
        user["_id"] = str(user["_id"])
        # Add the user to our list
        users.append(User(**user))

    return users

def update_user(user_id: str, user_update: UserUpdate) -> Optional[User]:
    """Update a user's information"""
    # Validate the user ID format
    if not ObjectId.is_valid(user_id):
        return None

    # Only update fields that were actually provided (not None)
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}

    # If no data to update, just return the current user
    if not update_data:
        return get_user_by_id(user_id)

    # Update the user in the database
    users_collection.update_one(
        {"_id": ObjectId(user_id)},  # Find the user by ID
        {"$set": update_data}        # Set the new values
    )

    # Return the updated user
    return get_user_by_id(user_id)

def delete_user(user_id: str) -> bool:
    """Delete a user from the database"""
    # Validate the user ID format
    if not ObjectId.is_valid(user_id):
        return False

    # Delete the user from the database
    result = users_collection.delete_one({"_id": ObjectId(user_id)})

    # Return True if a user was actually deleted, False if not found
    return result.deleted_count > 0
