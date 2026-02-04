from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from schemas import UserCreate, UserLogin, UserUpdate
from models import User, UsedToken
from utils import hash_password, verify_password, send_reset_email
from jose import JWTError, jwt
from utils import SECRET_KEY, ALGORITHM, create_access_token
from schemas import ForgotPasswordRequest, ResetPasswordRequest
import hashlib

# Create tables on first import
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")

router = APIRouter(prefix="/auth", tags=["Auth"])


def is_token_used(token: str, db: Session) -> bool:
    """Check if reset token has been used"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return db.query(UsedToken).filter(UsedToken.token_hash == token_hash).first() is not None


def mark_token_as_used(token: str, user_email: str, db: Session):
    """Mark reset token as used"""
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    used_token = UsedToken(token_hash=token_hash, user_email=user_email)
    db.add(used_token)
    db.commit()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Validate password confirmation
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check email exist
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user with hashed pwd
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    # Save to db
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    # Verifications
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create jwt token
    return {
        "access_token": create_access_token({"sub": db_user.email}),
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "address": db_user.address,
            "gender": db_user.gender,
            "age": db_user.age,
        }
    }


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """Send password reset email to user"""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            return {
                "message": "Password reset link has been sent.",
                "success": True
            }

        # Generate reset token
        token = create_access_token(
            {"sub": user.email, "type": "password_reset"},
            expires_delta=timedelta(minutes=10)
        )
        reset_link = f"http://localhost:5173/reset-password?token={token}"
        # Attempt to send email
        try:
            send_reset_email(user.email, reset_link)
            print(f"✅ Password reset email sent to {user.email}")
            return {
                "message": "Password reset link has been sent, please check.",
                "success": True
            }
        except Exception as email_error:
            print(f"❌ Email sending failed: {email_error}")
            # Still return success to not reveal if email exists
            return {
                "message": "Password reset link has been sent.",
                "success": True
            }
    except Exception as e:
        print(f"❌ Forgot password error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process password reset request"
        )


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset user password using token"""
    try:
        # Check if token has been used
        if is_token_used(data.token, db):
            raise HTTPException(status_code=400, detail="Reset link has already been used")
            
        # Decode and validate token
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        token_type = payload.get("type")
        if not email or token_type != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    try:
        # Find user and update password
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if new password is different from current password
        if verify_password(data.new_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be different from your current password"
            )

        # Mark token as used BEFORE updating password
        mark_token_as_used(data.token, user.email, db)
        
        # Update password
        user.password = hash_password(data.new_password)
        db.commit()

        print(f"✅ Password reset successful for {user.email}")
        return {
            "message": "Password reset successful.",
            "success": True
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Password reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )


@router.put("/profile")
def update_profile(user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update user profile information"""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        # Update only provided fields
        updated_fields = []
        if user_data.address is not None:
            user.address = user_data.address
            updated_fields.append("address")
        if user_data.gender is not None:
            user.gender = user_data.gender
            updated_fields.append("gender")
        if user_data.age is not None:
            user.age = user_data.age
            updated_fields.append("age")
        if not updated_fields:
            return {
                "message": "No changes made to profile",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "address": user.address,
                    "gender": user.gender,
                    "age": user.age,
                }
            }
        # Commit changes
        db.commit()
        db.refresh(user)
        print(f"✅ Profile updated for {user.email}: {', '.join(updated_fields)}")
        return {
            "message": f"Updated successfully: {', '.join(updated_fields)}",
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "address": user.address,
                "gender": user.gender,
                "age": user.age,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"❌ Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )