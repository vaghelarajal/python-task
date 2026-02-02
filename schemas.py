from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    email: EmailStr  # To identify the user
    address: str | None = None
    gender: str | None = None
    age: int | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)
