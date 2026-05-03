from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

async def verify_google_token(token: str) -> dict:
    """
    Verify Google ID token and return user info

    Returns:
        dict with: email, name, picture, google_id
    """
    try:
        # Verify the token with clock skew tolerance
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )

        # Token is valid, extract user info
        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture"),
            "google_id": idinfo.get("sub")  # Google user ID
        }
    except ValueError as e:
        # Invalid token
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verifying Google token: {str(e)}"
        )
