from fastapi import APIRouter

from app.api.routes import analysis, health, chapters, stories, analyses


api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(analysis.router)
api_router.include_router(stories.router)
api_router.include_router(chapters.router)
api_router.include_router(analyses.router)

