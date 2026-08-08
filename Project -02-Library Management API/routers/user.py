from fastapi import APIRouter, HTTPException, Path,Depends
from pydantic_data.data_validation import User, UpdateUser

from sqlalchemy.orm import Session

from database import get_db
from models import User as UserModel
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()

@router.get("/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.post("/create")
def add_user(user: User, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(
        UserModel.id == user.id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    db_user = UserModel(
        id=user.id,
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User created successfully"
    }

@router.put("/{user_id}")
def update_user(
    user_id: str,
    updateuser: UpdateUser,
    db: Session = Depends(get_db)
):

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_data = updateuser.model_dump(exclude_unset=True)

    for key, value in new_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully"
    }

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }