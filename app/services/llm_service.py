from app.core.logging import logger
from app.models.issue import Issue
from app.utils.helpers import load_prompt, truncate_diff
from app.utils.openrouter_client import llm
from app.utils.parser import parse_llm_json_array


async def review_diff(prompt_name: str, diff: str) -> list[Issue]:
    template = load_prompt(prompt_name)
    prompt = template.format(diff=truncate_diff(diff))
    response = await llm.ainvoke(prompt)

    try:
        items = parse_llm_json_array(response.content)
        return [Issue(**item) for item in items]
    except Exception as exc:
        logger.warning(
            "Failed to parse %s agent response: %s",
            prompt_name,
            exc,
        )
        return []


async def generate_summary_text(
    issue_count: int,
    categories: list[str],
    issues_text: str,
) -> str:
    template = load_prompt("summary")
    prompt = template.format(
        issue_count=issue_count,
        categories=", ".join(categories) or "none",
        issues_text=issues_text or "No issues found.",
    )
    response = await llm.ainvoke(prompt)
    return str(response.content).strip()


