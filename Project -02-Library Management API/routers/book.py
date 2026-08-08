from fastapi import APIRouter, HTTPException, Path,Depends
from fastapi.responses import JSONResponse
from pydantic_data.data_validation import Book, UpdateBook
from sqlalchemy.orm import Session
from database import get_db
from models import Book as BookModel

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/")
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()
    return books

@router.get("/{book_id}")
def get_single_book(
    book_id: str = Path(..., examples=["B001"]),
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book

@router.post("/create")
def addbook(book: Book, db: Session = Depends(get_db)):
    existing_book = db.query(BookModel).filter(BookModel.id == book.id).first()

    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="Book with this ID already exists"
        )
    
    db_book = BookModel(
        id=book.id,
        title=book.title,
        author=book.author,
        totalcopies=book.totalcopies
    )
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    
    return JSONResponse(
    status_code=201,
    content={"message": "Book added successfully"}
    )

@router.put("/{book_id}")
def update_book(
    book_id: str,
    updatebook: UpdateBook,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    new_data = updatebook.model_dump(exclude_unset=True)

    for key, value in new_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return {
        "message": "Book updated successfully"
    }

@router.delete("/{book_id}")
def delete_book(
    book_id: str,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }