"""
Market Intelligence Bot — automated opportunity scanning.
For educational purposes only.

Analyzes market conditions and generates briefings using local AI.
"""

import logging
from datetime import datetime
from typing import Optional

log = logging.getLogger("market-intel")


def build_prompt(
    focus_areas: list[str],
    include_competitors: bool = False,
    report_style: str = "executive_brief",
) -> str:
    areas = ", ".join(focus_areas) if focus_areas else "general market trends"

    return f"""Generate a market intelligence briefing for {datetime.now().strftime('%B %d, %Y')}.

Focus areas: {areas}
Report style: {report_style}
{'Include competitor analysis.' if include_competitors else ''}

Structure your report as:
1. **Market Overview** — Key trends and movements
2. **Opportunities** — Actionable opportunities identified
3. **Risks** — Potential threats or concerns
4. **Recommendations** — Suggested actions

Keep it concise and actionable. Use bullet points."""


def run(model_client, config: Optional[dict] = None) -> str:
    config = config or {}

    prompt = build_prompt(
        focus_areas=config.get("focus_areas", ["AI tools", "privacy tech"]),
        include_competitors=config.get("include_competitors", False),
        report_style=config.get("report_style", "executive_brief"),
    )

    log.info("Generating market intelligence briefing")
    result = model_client.complete(
        prompt,
        system="You are a market analyst specializing in technology trends.",
    )
    log.info("Briefing generated (%d chars)", len(result))

    return result
