import asyncio
import os

from app.agents.architecture_agent import architecture_agent
from app.agents.performance_agent import performance_agent
from app.agents.quality_agent import quality_agent
from app.agents.security_agent import security_agent
from app.agents.summary_agent import summary_agent
from app.agents.testing_agent import testing_agent
from app.static_analysis.shared.registry import run_static_analysis
from app.visualizer.issue_mapper import map_static_analysis_results

SPECIALIST_AGENTS = [
    security_agent,
    quality_agent,
    performance_agent,
    testing_agent,
    architecture_agent,
]


async def run_specialist_agents(state):
    results = await asyncio.gather(
        *[agent(state) for agent in SPECIALIST_AGENTS]
    )

    merged = {}
    for result in results:
        merged.update(result)

    static_root = os.environ.get("STATIC_ANALYSIS_ROOT")
    if static_root:
        static_analysis_results = run_static_analysis(static_root)
        merged["security_issues"] = list(
            merged.get("security_issues", [])
        ) + map_static_analysis_results(
            static_analysis_results["security"], "SECURITY"
        )
        merged["quality_issues"] = list(
            merged.get("quality_issues", [])
        ) + map_static_analysis_results(
            static_analysis_results["quality"], "QUALITY"
        )

    return merged


NODE_FUNCTIONS = {
    "run_specialist_agents": run_specialist_agents,
    "summary_agent": summary_agent,
}
