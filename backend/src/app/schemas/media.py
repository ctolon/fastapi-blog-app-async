from typing import Optional, List

from pydantic import BaseModel

class SingleMedia(BaseModel):
    filename: str
    
class MultiMedia(BaseModel):
    filenames: List[str]