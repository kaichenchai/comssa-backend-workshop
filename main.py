from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

# Import our database and models
from database import ping_database
from models import User, UserCreate, UserUpdate
import crud

# Create FastAPI instance
app = FastAPI(
    title="My Awesome FastAPI App with MongoDB",
    description="This FastAPI application now has a brain (database)!",
    version="2.0.0",
)

@app.on_event("startup")
def startup_event():
    """Test database connection when the app starts"""
    ping_database()

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Hello World! Now with MongoDB power!",
        "database": "Connected to MongoDB Atlas",
        "version": "2.0.0"
    }

# Create a new user (POST)
@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    """Create a new user in the database"""
    try:
        return crud.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all users (GET)
@app.get("/users/", response_model=List[User])
def get_users():
    """Get all users from the database"""
    return crud.get_all_users()

# Get a specific user (GET with path parameter)
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    """Get a specific user by their ID"""
    user = crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user (PUT with path parameter and request body)
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user_update: UserUpdate):
    """Update a user's information"""
    user = crud.update_user(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete a user (DELETE with path parameter)
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    """Delete a user from the database"""
    success = crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Health check endpoint
@app.get("/health")
def health_check():
    """Check if the app and database are healthy"""
    db_healthy = ping_database()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }
