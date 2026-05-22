from fastapi import FastAPI

from app.api.routes.health_routes import router as health_router
from app.api.routes.home_routes import router as home_router
from app.api.routes.review_routes import router as review_router

app = FastAPI(
    title="AI PR Reviewer",
    version="1.0.0",
    description="Multi-agent AI pull request reviewer",
)

app.include_router(home_router)
app.include_router(health_router)
app.include_router(review_router)
