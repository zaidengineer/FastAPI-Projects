from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from models import User, RevokedToken
import jwt
from datetime import datetime, timezone,timedelta
from schemas import SignupRequest, RefreshTokenRequest, ForgotPasswordRequest, ResetPasswordRequest
from security import hash_password,hash_reset_token,create_reset_token, verify_password, create_access_token,create_refresh_token,SECRET_KEY,ALGORITHM

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED
)
def signup(
    data:SignupRequest,
    db:Session=Depends(get_db)
):
    existing_user=db.query(User).filter(
        User.email==data.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    existing_username=db.query(User).filter(
        User.username==data.username
    ).first()
    if existing_username:
        raise HTTPException(status_code= 400,detail="Username already taken")
    new_user=User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "message":"User registered successfully",
        "user":{
            "id":new_user.id,
            "username":new_user.username,
            "email":new_user.email,
            "role":new_user.role
        }
    }



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    password_correct = verify_password(
        form_data.password,
        user.password_hash
    )

    if not password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
    user_id=user.id
    )

    refresh_token = create_refresh_token(
        user_id=user.id
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        token_type = payload.get("type")

        if user_id is None:
            raise credentials_exception

        if token_type != "refresh":
            raise credentials_exception

        revoked_token = db.query(RevokedToken).filter(
            RevokedToken.token == data.refresh_token
        ).first()

        if revoked_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked"
            )

        user_id = int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    new_access_token = create_access_token(
        user_id=user.id
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



@router.post("/logout")
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )

    try:
        payload = jwt.decode(
            data.refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        token_type = payload.get("type")

        if token_type != "refresh":
            raise credentials_exception

        expires_at = datetime.fromtimestamp(
            payload["exp"],
            tz=timezone.utc
        )

    except jwt.InvalidTokenError:
        raise credentials_exception

    existing_token = db.query(RevokedToken).filter(
        RevokedToken.token == data.refresh_token
    ).first()

    if existing_token:
        return {
            "message": "Already logged out"
        }

    revoked_token = RevokedToken(
        token=data.refresh_token,
        expires_at=expires_at
    )

    db.add(revoked_token)
    db.commit()

    return {
        "message": "Logout successful"
    }


@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    # Do not reveal whether the email exists
    if not user:
        return {
            "message": "If the email exists, a password reset link has been sent."
        }

    reset_token = create_reset_token()

    user.reset_token_hash = hash_reset_token(reset_token)

    user.reset_token_expires = (
        datetime.now(timezone.utc) + timedelta(minutes=15)
    )

    db.commit()

    # TEMPORARY FOR TESTING
    return {
        "message": "Password reset token generated",
        "reset_token": reset_token
    }



@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    token_hash = hash_reset_token(data.token)

    user = db.query(User).filter(
        User.reset_token_hash == token_hash
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    if not user.reset_token_expires:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Get current UTC time
    now = datetime.now(timezone.utc)

    # Handle MySQL naive datetime
    reset_expiry = user.reset_token_expires

    if reset_expiry.tzinfo is None:
        reset_expiry = reset_expiry.replace(
            tzinfo=timezone.utc
        )

    # Check expiration
    if reset_expiry < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    # Change password
    user.password_hash = hash_password(
        data.new_password
    )

    # Invalidate reset token
    user.reset_token_hash = None
    user.reset_token_expires = None

    db.commit()

    return {
        "message": "Password reset successfully"
    }