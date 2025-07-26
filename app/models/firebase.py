import firebase_admin
from firebase_admin import credentials, firestore, auth
from pathlib import Path
import os
import json
from fastapi import HTTPException


firebase_creds = "/etc/secrets/skillissue-ea816-firebase-adminsdk-fbsvc-8cc10a29d9.json"
if firebase_creds:
    cred_dict = json.loads(firebase_creds)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
else:
    firebase_admin.initialize_app()

db = firestore.client()

def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print("Token verification failed:", str(e))
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
        raise HTTPException(status_code=404, detail="Pardon, that user doesnt exist")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Idk what went wrong but {str(e)}")
