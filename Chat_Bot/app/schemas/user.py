from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class UserResponse(BaseModel):
    _id: str
    name: str
    email: EmailStr
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}