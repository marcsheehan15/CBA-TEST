from pydantic import BaseModel
from typing import Optional, List, Dict


class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Dict[str, Optional[int]]] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[Dict[str, Optional[int]]]] = None
    status: str
