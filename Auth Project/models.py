from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(
    primary_key=True,index=True)
    username: Mapped[str]=mapped_column(
        String(50), unique=True, nullable=False
    )
    email:Mapped[str]=mapped_column(
       String(50), unique=True,nullable=False
    )
    password_hash:Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )
    role:Mapped[str]=mapped_column(
        String(20),
        default="user",
        nullable=False
    )
    
    reset_token_hash = Column(
        String(255), nullable=True
    )

    reset_token_expires = Column(
        DateTime, nullable=True
    )




class RevokedToken(Base):
    __tablename__="revoked_tokens"
    id=Column(Integer, primary_key=True, index=True)
    token=Column(String(500),unique=True,nullable=False)
    expires_at=Column(DateTime, nullable=False)

