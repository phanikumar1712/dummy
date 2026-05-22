from fastapi import FastAPI

from app.api.routes.review_routes import (
    router as review_router
)

from app.api.routes.health_routes import (
    router as health_router
)

app = FastAPI(

    title="AI PR Reviewer",

    version="1.0.0"
)

app.include_router(review_router)

app.include_router(health_router)