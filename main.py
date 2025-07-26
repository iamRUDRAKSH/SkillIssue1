from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth
from app.routes import onboard
import os

app = FastAPI(title="SkillIssue Backend API", version="1.0.0")

origins = [
    "http://localhost:5173",  # React app
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Can be ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "dev_secret"))

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(onboard.router, prefix="/onboard", tags=["onboard"])

@app.get("/")
def home():
    return {"message": "I hope this works "}
