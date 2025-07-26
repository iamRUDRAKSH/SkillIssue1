from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from app.models.firebase import get_user_details
from typing import List, Dict, Optional
from google.cloud import firestore
from app.models.firebase import db
from app.models.Qdrant import client
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct

model = SentenceTransformer("all-MiniLM-L6-v2")
router = APIRouter()

# ----- Schemas -----

class ProjectSchema(BaseModel):
    title: str
    description: str
    tech_stack: List[str]
    requirements: List[str]

class OnboardingRequest(BaseModel):
    name: str
    email: str
    photo_url: Optional[str] = Field(
        default=None,
        description="URL of user's avatar; null if not provided"
    )
    skills: Optional[List[str]] = Field(
        default=None,
        description="List of skill IDs; null if none"
    )
    preferences: Optional[List[str]] = Field(
        default=None,
        description="List of preference IDs; null if none"
    )
    projects: Optional[Dict[str, ProjectSchema]] = Field(
        default=None,
        description="Map project_id → project details; null if none"
    )

# ----- Route -----

@router.post("/register")
def onboardUser(request: Request, data: OnboardingRequest):
    uid = request.session.get("user_uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Not verified, innit")
    else:
        userdetails = get_user_details(uid)
        print(userdetails)
        user_ref = db.collection("users").document(uid)

        # Build the payload, omitting any None fields
        payload = {
            "name": data.name,
            "email": data.email,
            "onboarded": True,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        if data.photo_url is not None:
            payload["photo_url"] = data.photo_url
        if data.skills is not None:
            payload["skills"] = data.skills
        if data.preferences is not None:
            payload["preferences"] = data.preferences
        if data.projects is not None:
            payload["projects"] = {pid: proj.dict() for pid, proj in data.projects.items()}

        # Merge into user document
        user_ref.set(payload, merge=True)

        # Optionally handle user_skills and user_preferences only if provided
        batch = db.batch()
        if data.skills:
            for skill_id in data.skills:
                us_ref = db.collection("user_skills").document()
                batch.set(us_ref, {
                    "uid": user_ref,
                    "skill_id": db.collection("skills").document(skill_id)
                })
        if data.preferences:
            for pref_id in data.preferences:
                up_ref = db.collection("user_preferences").document()
                batch.set(up_ref, {
                    "uid": user_ref,
                    "pref_id": db.collection("preferences").document(pref_id)
                })
        if data.skills or data.preferences:
            batch.commit()

        # ---- 🔥 VECTOR EMBEDDING SECTION ----

        # Embed and store user vector in Uid_Skills
        skills_text = " ".join(data.skills) if data.skills else ""
        pref_text = " ".join(data.preferences) if data.preferences else ""
        combined_user_text = f"{skills_text} {pref_text}"

        user_vector = model.encode(combined_user_text, normalize_embeddings=True)

        client.upsert(
            collection_name="Uid_Skills",
            points=[
                PointStruct(
                    id=uid,
                    vector=user_vector,
                    payload={
                        "uid": uid,
                        "skills": data.skills,
                        "preferences": data.preferences
                    }
                )
            ]
        )

        # Embed and store project vectors
        if data.projects:
            for pid, proj in data.projects.items():
                req_text = " ".join(proj.requirements)
                tech_text = " ".join(proj.tech_stack)

                req_vector = model.encode(req_text, normalize_embeddings=True)
                tech_vector = model.encode(tech_text, normalize_embeddings=True)

                # Project requirement vector
                client.upsert(
                    collection_name="Pid_Requirement",
                    points=[
                        PointStruct(
                            id=pid,
                            vector=req_vector,
                            payload={
                                "pid": pid,
                                "title": proj.title,
                                "description": proj.description,
                                "requirements": proj.requirements
                            }
                        )
                    ]
                )

                # Project tech stack vector
                client.upsert(
                    collection_name="Pid_TechStack",
                    points=[
                        PointStruct(
                            id=pid,
                            vector=tech_vector,
                            payload={
                                "pid": pid,
                                "title": proj.title,
                                "description": proj.description,
                                "tech_stack": proj.tech_stack
                            }
                        )
                    ]
                )

        return {"message": "Onboarding complete", "uid": uid}