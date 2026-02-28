"""
Content Generator Bot — automated marketing content.
For educational purposes only.

Generates platform-specific marketing posts using local AI.
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional

log = logging.getLogger("content-bot")

PLATFORMS = {
    "twitter": {
        "max_length": 280,
        "style": "punchy, conversational, uses hooks",
    },
    "telegram": {
        "max_length": 4096,
        "style": "detailed, informative, uses formatting",
    },
    "linkedin": {
        "max_length": 3000,
        "style": "professional, thought-leadership, uses line breaks",
    },
}


def build_prompt(
    topic: str,
    platforms: list[str],
    tone: str = "professional",
    brand_voice: str = "",
) -> str:
    platform_specs = []
    for p in platforms:
        spec = PLATFORMS.get(p, {"max_length": 500, "style": "general"})
        platform_specs.append(
            f"- {p.upper()}: max {spec['max_length']} chars, style: {spec['style']}"
        )

    return f"""Generate marketing content for today ({datetime.now().strftime('%B %d, %Y')}).

Topic: {topic}
Tone: {tone}
{f'Brand voice: {brand_voice}' if brand_voice else ''}

Platforms:
{chr(10).join(platform_specs)}

For each platform, provide:
1. A hook/opening line
2. Body content (platform-appropriate length)
3. Call to action

Format as JSON:
{{"posts": [{{"platform": "...", "content": "...", "hashtags": [...]}}]}}"""


def parse_output(raw: str) -> list[dict]:
    """Extract structured post data from model output."""
    try:
        # Try direct JSON parse
        data = json.loads(raw)
        return data.get("posts", [data] if "platform" in data else [])
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from markdown code block
    if "```" in raw:
        start = raw.find("```json")
        if start == -1:
            start = raw.find("```")
        start = raw.find("\n", start) + 1
        end = raw.find("```", start)
        if start > 0 and end > start:
            try:
                data = json.loads(raw[start:end])
                return data.get("posts", [data])
            except json.JSONDecodeError:
                pass

    return [{"platform": "raw", "content": raw}]


def run(model_client, config: Optional[dict] = None) -> list[dict]:
    """Execute content generation."""
    config = config or {}
    topic = config.get("topic", "private AI and data sovereignty")
    platforms = config.get("platforms", ["twitter", "telegram"])
    tone = config.get("tone", "professional but accessible")
    brand_voice = config.get("brand_voice", "")

    prompt = build_prompt(topic, platforms, tone, brand_voice)

    log.info("Generating content for %s", ", ".join(platforms))
    raw = model_client.complete(prompt, system="You are a marketing content specialist.")
    posts = parse_output(raw)
    log.info("Generated %d posts", len(posts))

    return posts
