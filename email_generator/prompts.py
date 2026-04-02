from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from email_generator.config import Settings

SYSTEM_PROMPT = """\
You are an expert direct-response email copywriter specialising in affiliate marketing \
emails for the make-money-online (MMO) and internet marketing niches. You write emails that:
- Sound like they come from a real person, not a corporate marketer
- Use plain, conversational language that resonates with beginners
- Follow proven direct-response structures (AIDA, PAS, or story-based)
- Have strong, specific subject lines with high open-rate potential
- Include a single clear call-to-action linking to the affiliate offer
- Are between 150-350 words in the body (not too short, not too long)
- Avoid spam trigger words (free money, guaranteed income, make money fast)

The product being promoted is WiFi Profits, a WarriorPlus software that helps beginners:
1. Find high-converting affiliate offers on WarriorPlus
2. Clone and customise sales pages ("money pages") with their affiliate links
3. Generate traffic using AI content tools, viral video creation, and social media

Always output your response in EXACTLY this format — no preamble, no explanation:
SUBJECT: <the subject line>
---HTML---
<the full HTML email body using only simple <p>, <strong>, <a> tags>
---PLAIN---
<plain text version of the same email, no HTML tags>
---END---
"""

SLOT_CONFIGS: dict[str, dict[str, str]] = {
    "morning": {
        "angle": "curiosity/story hook",
        "subject_direction": (
            "Tell a short relatable story (1-2 sentences) about someone failing at "
            "side hustles before finding this. Do NOT reveal the product name in the subject line."
        ),
        "body_direction": (
            "Open with the story, build curiosity, reveal WiFi Profits as the solution "
            "mid-email. Tone: warm, conversational, personal."
        ),
        "cta_style": "soft — e.g. 'Check it out here' or 'See what I mean'",
    },
    "afternoon": {
        "angle": "proof/results-focused",
        "subject_direction": (
            "Lead with a specific result or number (e.g. commissions earned, pages cloned, "
            "time saved). Keep it believable for a beginner."
        ),
        "body_direction": (
            "Lead with a concrete result claim, explain the mechanism (clone pages, "
            "WarriorPlus offers, AI traffic), then show how easy it is for beginners."
        ),
        "cta_style": "direct — e.g. 'Get access now' or 'Grab your copy here'",
    },
    "evening": {
        "angle": "urgency/fear-of-missing-out",
        "subject_direction": (
            "Use urgency or scarcity language (limited bonuses, price going up, closing soon). "
            "Must feel authentic, not spammy."
        ),
        "body_direction": (
            "Remind the reader this is a limited window, list the key bonuses they lose by "
            "waiting, and make a final strong case for acting tonight."
        ),
        "cta_style": "urgent — e.g. 'Don't miss out — click here now' or 'Last chance to grab the bonuses'",
    },
}

SLOT_NUMBER = {"morning": 1, "afternoon": 2, "evening": 3}


def build_prompt(slot: str, settings: Settings) -> str:
    cfg = SLOT_CONFIGS[slot]
    today = date.today().isoformat()
    return f"""\
Today is {today}. Write a {slot} marketing email using the following parameters:

- Persuasion angle: {cfg["angle"]}
- Subject line direction: {cfg["subject_direction"]}
- Body direction: {cfg["body_direction"]}
- Call-to-action style: {cfg["cta_style"]}
- Sender name (sign-off): {settings.sender_name}
- Target audience: {settings.audience}
- Affiliate link (use this as the href for every CTA): {settings.affiliate_link}
- Do not repeat content you might have written for other slots today — this email \
should feel distinctly different in angle, hook, and structure.
"""
