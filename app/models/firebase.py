import firebase_admin
from firebase_admin import credentials, firestore, auth
from fastapi import HTTPException
import os
from pathlib import Path

# Path to your service‑account JSON file (mounted or env‑configured)
FIREBASE_CRED_PATH = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    "/etc/secrets/skillissue-ea816-firebase-adminsdk-fbsvc-8cc10a29d9.json"
)

# Initialize Firebase Admin
if Path(FIREBASE_CRED_PATH).is_file():
    # Directly pass the path to credentials.Certificate
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred)
else:
    # Fallback to default application credentials
    firebase_admin.initialize_app()

db = firestore.client()

def verify_token(id_token: str):
    try:
        return auth.verify_id_token(id_token)
    except Exception as e:
        # log if needed
        return None

def get_user_details(user_uid: str):
    try:
        user = auth.get_user(user_uid)
        return {
            "email": user.email,
            "name": user.display_name,
            "photo_url": user.photo_url
        }
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}")