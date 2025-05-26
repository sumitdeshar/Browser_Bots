from typing import Optional, List
from pydantic import BaseModel

class Message(BaseModel):
    message: str
    userid: str
    book_list: Optional[List[str]] = None
