from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from app.models.firebase import get_user_details 
router = APIRouter()

class OnboardingRequest(BaseModel):
    name: str
    photo_url: str
    skills: List[str]
    preferences: List[str]
    projects: Dict[str, str, List[str], List[str]]

@router.post("/register")
def onboardUser(request: Request):
    uid = request.session.get("user_uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Not verified, innit")
    else:
        userdetails = get_user_details(uid)
        print(userdetails)
    