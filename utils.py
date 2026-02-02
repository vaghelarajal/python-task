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


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def send_reset_email(email: str, reset_link: str):
    """Send password reset email using SMTP"""
    
    # Check if email credentials are configured
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("❌ Email credentials not configured in .env file")
        print(f"\n========== PASSWORD RESET LINK (CONSOLE) ==========")
        print(f"Reset link for {email}:")
        print(reset_link)
        print("==================================================\n")
        raise Exception("Email credentials not configured")
    
    try:
        print(f"📧 Attempting to send email to {email}...")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "🔐 Password Reset Request - Your App"
        
        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Hello!</h2>
                    <p>You requested a password reset for your account. Click the button below to reset your password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset My Password</a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Important:</strong> This link will expire in <strong>10 minutes</strong> for security reasons.
                    </div>
                    
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #e9ecef; padding: 10px; border-radius: 5px;">
                        {reset_link}
                    </p>
                    
                    <p>If you didn't request this password reset, please ignore this email. Your password will remain unchanged.</p>
                    
                    <p>Best regards,<br>Your App Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        text_body = f"""
        Password Reset Request
        
        Hello!
        
        You requested a password reset for your account. Click the link below to reset your password:
        
        {reset_link}
        
        ⚠️ IMPORTANT: This link will expire in 10 minutes for security reasons.
        
        If you didn't request this password reset, please ignore this email. Your password will remain unchanged.
        
        Best regards,
        Your App Team
        
        ---
        This is an automated message. Please do not reply to this email.
        """
        
        # Attach both HTML and text versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Connect to Gmail SMTP server
        print("🔗 Connecting to Gmail SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS encryption
        
        print("🔐 Authenticating with Gmail...")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        print("📤 Sending email...")
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        
        print(f"✅ Password reset email successfully sent to {email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Gmail authentication failed!")
        print("💡 Make sure you're using an App Password, not your regular Gmail password")
        print("💡 Enable 2-Factor Authentication and generate an App Password at:")
        print("   https://myaccount.google.com/apppasswords")
        raise Exception("Gmail authentication failed - check your app password")
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error occurred: {e}")
        raise Exception(f"Failed to send email via SMTP: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error sending email: {e}")
        print(f"\n========== FALLBACK: PASSWORD RESET LINK ==========")
        print(f"Reset link for {email}:")
        print(reset_link)
        print("==================================================\n")
        raise Exception(f"Failed to send email: {e}")
