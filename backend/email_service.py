"""
Email service for sending verification emails.
Uses Resend API for email delivery.
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional
import resend
from config import settings


# Initialize Resend API key
if settings.RESEND_API_KEY:
    resend.api_key = settings.RESEND_API_KEY


def generate_verification_token() -> str:
    """Generate a secure random verification token."""
    return secrets.token_urlsafe(32)


def send_verification_email(email: str, token: str, name: str) -> bool:
    """
    Send verification email to user.
    
    Args:
        email: User's email address
        token: Verification token
        name: User's name
        
    Returns:
        True if email sent successfully, False otherwise
    """
    if not settings.RESEND_API_KEY or not settings.FROM_EMAIL:
        print(f"[EMAIL SERVICE] Verification email would be sent to {email} with token: {token}")
        print("[EMAIL SERVICE] Configure RESEND_API_KEY and FROM_EMAIL to enable email sending")
        return True  # Return True for development
    
    try:
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Welcome to University Dating App, {name}!</h2>
            <p>Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>Or copy this link: {verification_url}</p>
            <p>This link will expire in 24 hours.</p>
        </body>
        </html>
        """
        
        params = {
            "from": settings.FROM_EMAIL,
            "to": [email],
            "subject": "Verify Your Email - University Dating App",
            "html": html_content
        }
        
        email_response = resend.Emails.send(params)
        print(f"[EMAIL SERVICE] Verification email sent to {email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL SERVICE] Error sending email: {e}")
        return False


def get_verification_token_expiry() -> datetime:
    """Get the expiry time for verification token (24 hours from now)."""
    return datetime.utcnow() + timedelta(hours=24)
