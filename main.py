from fastapi import FastAPI
from settings.config import settings
from api.users.routers import user_router
from api.jobs.routers import jobs_router

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
app.include_router(user_router)
app.include_router(jobs_router)
