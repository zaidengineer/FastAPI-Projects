from typing import Optional,Annotated
from pydantic import BaseModel,Field,EmailStr

class Book(BaseModel):
    id:Annotated[str,Field(..., min_length=3, max_length=8)]
    title:Annotated[str,Field(..., min_length=3, max_length=20)]
    author:Annotated[str,Field(..., min_length=3, max_length=20)]
    totalcopies:Annotated[int,Field(..., ge=0)]

class UpdateBook(BaseModel):
    title: Annotated[Optional[str],Field(min_length=3, max_length=20)] = None
    author:Annotated[Optional[str],Field(min_length=3, max_length=20)] = None
    totalcopies:Annotated[Optional[int],Field(ge=0)] = None

class Borrow(BaseModel):
    user_id:Annotated[str,Field(..., description="User id")]
    book_id:Annotated[str, Field(..., description="Book id")]

    
class User(BaseModel):
    id: Annotated[str, Field(..., min_length=3, max_length=8)]
    name: Annotated[str, Field(..., min_length=3, max_length=20)]
    email: Annotated[EmailStr, Field(...)]


class UpdateUser(BaseModel):
    name: Annotated[Optional[str], Field(default=None, min_length=4, max_length=20)]
    email: Annotated[Optional[EmailStr], Field(default=None)]