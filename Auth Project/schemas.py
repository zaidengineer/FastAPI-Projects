from pydantic import BaseModel,EmailStr,Field


class SignupRequest(BaseModel):
    username:str=Field(
        min_length=3,max_length=50
    )
    email:EmailStr
    password:str=Field(
        min_length=8,
        max_length=100
    )

class LoginRequest(BaseModel):

    email: EmailStr

    password: str

class RefreshTokenRequest(BaseModel):

    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)