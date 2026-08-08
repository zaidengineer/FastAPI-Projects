from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Date,
    ForeignKey,
)

from database import Base
class Book(Base):
    __tablename__ = "books"

    id = Column(String(10), primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    totalcopies = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


class Borrow(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        String(10),
        ForeignKey("users.id"),
        nullable=False
    )

    book_id = Column(
        String(10),
        ForeignKey("books.id"),
        nullable=False
    )

    borrowdate = Column(Date, nullable=False)

    returned = Column(Boolean, default=False)

    copies = Column(Integer, default=1)