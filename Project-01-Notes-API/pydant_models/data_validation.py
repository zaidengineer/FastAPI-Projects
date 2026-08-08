from pydantic import BaseModel,Field
from typing import Optional,Annotated,List

class Notes(BaseModel):
    id:Annotated[str,Field(..., min_length=3, max_length=12, description="Notes id")]
    title:Annotated[str,Field(..., min_length=3, max_length=20, description="Notes Title")]
    content:Annotated[str,Field(..., min_length=5, max_length=200)]
    category:Annotated[str,Field(..., min_length=3, max_length=100, description="Notes Category")]
    tags:Annotated[List[str],Field(..., description="Tags list")]

class Notes_update(BaseModel):
    id:Optional[str]=None
    tittle:Annotated[Optional[str],Field(min_length=3, max_length=20)] = None
    content:Optional[str]=None
    category:Optional[str]=None
    tags:Optional[List[str]]=None

class Pinned(BaseModel):
    is_pinned:bool