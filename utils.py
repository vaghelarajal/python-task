from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_CHANGE_THIS")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def send_reset_email(email: str, reset_link: str):
    """Send password reset email with HTML template and clickable links"""
    # Quick credential check
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print(f" Email not configured, reset link: {reset_link}")
        return False
    try:
        # Create email with HTML template
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Password Reset Request"
        
        # HTML email template with clickable link
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">Password Reset Request</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; border: 1px solid #e9ecef;">
                <p style="font-size: 16px; margin-bottom: 20px;">Hello,</p>
                
                <p style="font-size: 16px; margin-bottom: 25px;">
                    We received a request to reset your password. Click the button below to create a new password:
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" 
                       style="background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 16px; font-weight: bold; display: inline-block; box-shadow: 0 2px 4px rgba(0,123,255,0.3);">
                        Reset My Password
                    </a>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 25px;">
                    Or copy and paste this link in your browser:<br>
                    <a href="{reset_link}" style="color: #007bff; word-break: break-all;">{reset_link}</a>
                </p>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0; font-size: 14px; color: #856404;">
                        <strong>⚠️ Important:</strong> This link expires in 10 minutes for security reasons.
                    </p>
                </div>
                
                <p style="font-size: 14px; color: #666; margin-top: 25px;">
                    If you didn't request this password reset, please ignore this email. Your password will remain unchanged.
                </p>
                
                <hr style="border: none; border-top: 1px solid #e9ecef; margin: 25px 0;">
                
                <p style="font-size: 12px; color: #999; text-align: center; margin: 0;">
                    This is an automated message, please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
Password Reset Request

We received a request to reset your password.

Click this link to reset your password:
{reset_link}

This link expires in 10 minutes.

If you didn't request this, please ignore this email.
        """
        
        # Attach both HTML and plain text versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Quick SMTP connection with timeout
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        print(f" HTML email sent to {email}")
        return True
    except Exception as e:
        print(f" Email failed: {e}")
        print(f"Reset link: {reset_link}")
        return False
