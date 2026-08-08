from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic_data.data_validation import Borrow
from datetime import date

from sqlalchemy.orm import Session

from database import get_db
from models import (
    Book as BookModel,
    User as UserModel,
    Borrow as BorrowModel
)

router = APIRouter(
    prefix="/borrow",
    tags=["Borrow"]
)

@router.post("/borrow")
def borrow_book(
    borrow: Borrow,
    db: Session = Depends(get_db)
):

    user = db.query(UserModel).filter(
        UserModel.id == borrow.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    book = db.query(BookModel).filter(
        BookModel.id == borrow.book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book.totalcopies <= 0:
        raise HTTPException(
            status_code=400,
            detail="Book is out of stock"
        )

    already_borrowed = (
        db.query(BorrowModel)
        .filter(
            BorrowModel.user_id == borrow.user_id,
            BorrowModel.book_id == borrow.book_id,
            BorrowModel.returned == False
        )
        .first()
    )

    if already_borrowed:
        raise HTTPException(
            status_code=400,
            detail="Book already borrowed"
        )

    borrow_record = BorrowModel(
        user_id=borrow.user_id,
        book_id=borrow.book_id,
        borrowdate=date.today(),
        returned=False,
        copies=1
    )

    book.totalcopies -= 1

    db.add(borrow_record)
    db.commit()

    return JSONResponse(
        status_code=201,
        content={
            "message": "Book borrowed successfully"
        }
    )


@router.post("/return")
def return_book(
    borrow: Borrow,
    db: Session = Depends(get_db)
):

    borrow_record = (
        db.query(BorrowModel)
        .filter(
            BorrowModel.user_id == borrow.user_id,
            BorrowModel.book_id == borrow.book_id,
            BorrowModel.returned == False
        )
        .first()
    )

    if not borrow_record:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    borrow_record.returned = True

    book = db.query(BookModel).filter(
        BookModel.id == borrow.book_id
    ).first()

    book.totalcopies += 1

    db.commit()

    return {
        "message": "Book returned successfully"
    }


@router.get("/")
def borrow_history(
    db: Session = Depends(get_db)
):
    return db.query(BorrowModel).all()