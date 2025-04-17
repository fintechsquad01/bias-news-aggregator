from fastapi import APIRouter

from app.api.api_v1.endpoints import news, health, analysis, metadata

api_router = APIRouter()
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
