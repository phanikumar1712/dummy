from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from app.models.request_models import ReviewRequest
from app.models.response_models import ReviewResponse
from app.services.review_service import run_pr_review

router = APIRouter()


@router.post("/review", response_model=ReviewResponse)
async def review_pr(data: ReviewRequest):
    try:
        return await run_pr_review(data.pr_url)
    except ValueError as e:
        logger.warning("Invalid request: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("PR review failed")
        raise HTTPException(status_code=500, detail=str(e)) from e
