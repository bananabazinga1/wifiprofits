import logging
import anthropic

from email_generator.config import settings
from email_generator.prompts import SYSTEM_PROMPT, build_prompt

logger = logging.getLogger(__name__)


def _parse_section(text: str, start_marker: str, end_marker: str) -> str:
    start = text.find(start_marker)
    end = text.find(end_marker, start)
    if start == -1 or end == -1:
        return ""
    return text[start + len(start_marker):end]


def generate_email(slot: str) -> tuple[str, str, str]:
    """Call the Claude API and return (subject, html_body, plain_body)."""
    prompt = build_prompt(slot, settings)
    client = anthropic.Anthropic(api_key=settings.api_key)

    message = client.messages.create(
        model=settings.claude_model,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text
    logger.debug("Raw Claude response for slot '%s':\n%s", slot, raw)

    subject = _parse_section(raw, "SUBJECT:", "---HTML---").strip()
    html_body = _parse_section(raw, "---HTML---", "---PLAIN---").strip()
    plain_body = _parse_section(raw, "---PLAIN---", "---END---").strip()

    if not subject or not html_body or not plain_body:
        logger.warning(
            "Could not fully parse Claude response for slot '%s'. Raw output:\n%s",
            slot,
            raw,
        )

    return subject, html_body, plain_body
