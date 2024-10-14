from fastapi import APIRouter, Depends, HTTPException
from .schema import JobCreationRequest, JobFilter
from typing import Annotated
from api.users.utils import jwt_auth
from sqlalchemy.orm import Session
from db.session import LOCAL_SESSION
from .models import JobManager

jobs_router = APIRouter(prefix="/jobs", tags=["Jobs Management"])


def get_db():
    db = LOCAL_SESSION()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@jobs_router.post("/create")
async def create_job_post(
    user: Annotated[dict, Depends(jwt_auth)], db: db_dependency, job: JobCreationRequest
):
    job_post = JobManager.create_job(job=job, user_id=user.get("user_id"), db=db)
    if not job_post:
        raise HTTPException(status_code=500)
    return job_post


@jobs_router.get("/fetch")
async def get_job_posts(db: db_dependency, query: JobFilter = Depends()):

    return JobManager.get_job_posts(db, **query.model_dump())
