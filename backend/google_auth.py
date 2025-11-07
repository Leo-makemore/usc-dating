"""
Google OAuth authentication utilities.
Verifies Google OAuth tokens and extracts user email.
"""
from typing import Optional
from google.auth.transport import requests
from google.oauth2 import id_token
from config import settings


def verify_google_token(token: str) -> Optional[dict]:
    """
    Verify Google OAuth ID token and return user info.
    
    Args:
        token: Google OAuth ID token from frontend
        
    Returns:
        Dictionary with user info (email, name, etc.) or None if invalid
    """
    try:
        if not settings.GOOGLE_CLIENT_ID:
            # For development, try to decode token without verification
            # This is less secure but allows testing
            print("[WARNING] GOOGLE_CLIENT_ID not set. Attempting to decode token without verification.")
            try:
                # Try to decode JWT token without verification (for development only)
                # This allows testing when GOOGLE_CLIENT_ID is not set
                import base64
                import json
                
                # JWT has 3 parts separated by dots
                parts = token.split('.')
                if len(parts) != 3:
                    print("[GOOGLE AUTH] Invalid token format")
                    return None
                
                # Decode the payload (second part)
                payload = parts[1]
                # Add padding if needed
                padding = 4 - len(payload) % 4
                if padding != 4:
                    payload += '=' * padding
                
                decoded_bytes = base64.urlsafe_b64decode(payload)
                decoded = json.loads(decoded_bytes)
                
                print(f"[GOOGLE AUTH] Decoded token (dev mode): {decoded.get('email')}")
                
                return {
                    'email': decoded.get('email'),
                    'name': decoded.get('name'),
                    'picture': decoded.get('picture'),
                    'sub': decoded.get('sub')
                }
            except Exception as e:
                print(f"[GOOGLE AUTH] Failed to decode token: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        
        # Verify the issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError(f'Wrong issuer: {idinfo.get("iss")}')
        
        return {
            'email': idinfo.get('email'),
            'name': idinfo.get('name'),
            'picture': idinfo.get('picture'),
            'sub': idinfo.get('sub')  # Google user ID
        }
    except ValueError as e:
        print(f"[GOOGLE AUTH] Token verification failed (ValueError): {e}")
        import traceback
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"[GOOGLE AUTH] Error verifying token: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def validate_usc_email(email: str) -> bool:
    """
    Validate that email is from USC.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email ends with @usc.edu, False otherwise
    """
    return email and email.lower().endswith('@usc.edu')

