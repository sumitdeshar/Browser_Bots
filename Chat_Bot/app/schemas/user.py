


from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponseModel(BaseModel):
    _id: Optional[str]  # keep _id, but as a string
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # helps with ORM or dict conversion if needed
