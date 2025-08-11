from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# The parent class that contains all required information of a user: name, email and age
class UserBase(BaseModel):
    name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    age: int = Field(..., ge=0, le=150, description="User's age")

# This class represents an act of creating a new user in the database
# To create a new user, we basically need just name, email and age. Hence, we simply inherit this class from the base class
class UserCreate(UserBase):
    pass

# This is the actual user object stored in the database, apart from the required fields from the base class
# we also need an id to determine each users and created_at for auditing purpose
class User(UserBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

# This class represents the act of updating an existing user
# When updating a user, we may not update all of the user's information (e.g. we might just need to change the email)
# Therefore, all of these fields are optional and we only need to provide required fields that need to be changed
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
