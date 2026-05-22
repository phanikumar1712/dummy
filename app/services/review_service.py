from app.core.logging import logger
from app.github.fetch_pr import fetch_pr_diff, parse_pr_url
from app.github.review_pr import create_pr_review
from app.graph.workflow import graph
from app.models.response_models import ReviewResponse
from app.services.diff_parser_service import parse_diff_files
from app.services.review_message_service import generate_review_message
from app.utils.helpers import default_pr_state
from app.visualizer.review_output import build_structured_review


async def run_pr_review(pr_url: str, post_to_github: bool = True) -> ReviewResponse:
    logger.info("Starting PR review for %s", pr_url)

    diff = fetch_pr_diff(pr_url)
    parsed_files = parse_diff_files(diff)
    initial_state = default_pr_state(pr_url, diff, parsed_files)

    result = await graph.ainvoke(initial_state)
    structured = build_structured_review(
        summary=result["final_summary"],
        issues=result["all_issues"],
        folder_tree=result["folder_tree"],
    )

    review_message = generate_review_message(
        structured["issues"],
        folder_tree=structured["folder_tree"],
    )
    event_type = "REQUEST_CHANGES" if structured["issues"] else "APPROVE"

    if post_to_github:
        parsed_pr = parse_pr_url(pr_url)
        create_pr_review(
            owner=parsed_pr["owner"],
            repo=parsed_pr["repo"],
            pr_number=parsed_pr["pr_number"],
            body=review_message,
            event=event_type,
        )

    return ReviewResponse(**structured)
