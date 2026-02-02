from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserLogin, UserUpdate
from models import User
from utils import hash_password, verify_password, send_reset_email
from jose import JWTError, jwt
from utils import SECRET_KEY, ALGORITHM, create_access_token
from schemas import ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "access_token": create_access_token({"sub": db_user.email}),
        "user": {
            "username": db_user.username,
            "email": db_user.email,
            "address": db_user.address,
            "gender": db_user.gender,
            "age": db_user.age,
        }
    }


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate reset token (10 minutes expiry)
    token = create_access_token(
        {"sub": user.email},
        expires_delta=timedelta(minutes=10)
    )

    # Create reset link
    reset_link = f"http://localhost:5173/reset-password?token={token}"
    
    # Attempt to send email
    try:
        send_reset_email(user.email, reset_link)
        return {
            "message": "Password reset link has been sent to your email address. Please check your inbox.",
            "success": True
        }
    except Exception as e:
        # Log the error but don't expose internal details to user
        print(f"❌ Email sending failed: {e}")
        
        # Return a user-friendly message
        return {
            "message": "There was an issue sending the email. Please try again or contact support.",
            "success": False,
            "error": "Email delivery failed"
        }


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password reset successful"}


@router.put("/profile")
def update_profile(user_data: UserUpdate, db: Session = Depends(get_db)):
    # In a real app, you'd get user from JWT token
    # For now, we'll use email to identify user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.address is not None:
        user.address = user_data.address
    if user_data.gender is not None:
        user.gender = user_data.gender
    if user_data.age is not None:
        user.age = user_data.age
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Profile updated successfully",
        "user": {
            "username": user.username,
            "email": user.email,
            "address": user.address,
            "gender": user.gender,
            "age": user.age,
        }
    }