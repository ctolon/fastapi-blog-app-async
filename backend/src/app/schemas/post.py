from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

# Shared properties
class PostBase(BaseModel):
    image_url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    creator: Optional[str] = None
    timestamp: Optional[datetime] = None
    
# Properties to receive via API on creation
class PostCreate(PostBase):
    image_url: str
    title: str
    content: str
    creator: str

# Properties to receive via API on update
class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Post(PostInDBBase):
    pass


# Additional properties stored in DB
class PostInDB(PostInDBBase):
    pass