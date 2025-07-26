from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

client = QdrantClient(
    url="https://b76fa2ef-206e-4d71-afae-5dbbf666e1f6.eu-west-2-0.aws.cloud.qdrant.io",
    api_key=os.getenv("QDRANT_API_KEY", "error_key_not_found")
)

def create_collection_if_missing(name):
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

# User Vector Collection
create_collection_if_missing("Uid_Skills")

# Project Vectors
create_collection_if_missing("Pid_Requirement")
create_collection_if_missing("Pid_TechStack")