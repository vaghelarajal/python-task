from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern="^[A-Za-z]+$",
        description="Username must contain only letters and no whitespaces"
    )
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str
