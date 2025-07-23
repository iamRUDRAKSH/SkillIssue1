from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes import auth  # Make sure this import path is correct

import os
import uvicorn

app = FastAPI(title="SkillIssue Backend API", version="1.0.0")

origins = [
    "http://localhost:5173",  # React app origin; update to deployed frontend URL if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def home():
    return {"message": "I hope this works "}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
