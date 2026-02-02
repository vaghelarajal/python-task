#!/usr/bin/env python3
"""
Simple test script to verify email functionality
"""
import os
from dotenv import load_dotenv
from utils import send_reset_email

# Load environment variables
load_dotenv()

def test_email():
    """Test email sending functionality"""
    
    print("🧪 Testing Email Configuration...")
    print(f"📧 Email Address: {os.getenv('EMAIL_ADDRESS')}")
    print(f"🔐 Password Set: {'Yes' if os.getenv('EMAIL_PASSWORD') else 'No'}")
    
    # Test email
    test_email_address = os.getenv('EMAIL_ADDRESS')  # Send to yourself for testing
    test_reset_link = "http://localhost:5173/reset-password?token=test_token_123"
    
    if not test_email_address:
        print("❌ No email address configured in .env file")
        return False
    
    try:
        print(f"\n📤 Attempting to send test email to {test_email_address}...")
        send_reset_email(test_email_address, test_reset_link)
        print("✅ Email test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_email()
    if success:
        print("\n🎉 Email functionality is working correctly!")
        print("💡 You can now use the forgot password feature in your app.")
    else:
        print("\n⚠️  Email functionality needs attention.")
        print("💡 Check your Gmail App Password and 2FA settings.")