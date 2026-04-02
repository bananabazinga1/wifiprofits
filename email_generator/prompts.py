from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from email_generator.config import Settings

from email_generator.config import load_product_copy

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

The product being promoted is described in the PRODUCT COPY section of each message. \
Read that copy carefully to extract the product name, core promise, key features, bonuses, \
pricing, and any proof elements before writing. Do not invent details not present in the copy.

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
            "Open with the story, build curiosity, reveal the product as the solution "
            "mid-email — use the name and core promise from the PRODUCT COPY. "
            "Tone: warm, conversational, personal."
        ),
        "cta_style": "soft — e.g. 'Check it out here' or 'See what I mean'",
    },
    "afternoon": {
        "angle": "proof/results-focused",
        "subject_direction": (
            "Lead with a specific result or number (e.g. commissions earned, time saved, "
            "results achieved). Keep it believable for a beginner."
        ),
        "body_direction": (
            "Lead with a concrete result claim, explain the mechanism using the key features "
            "described in the PRODUCT COPY, then show how easy it is for beginners."
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

# Campaign arc definitions, keyed by (total_days, day_num).
# Each entry governs the narrative stage, sell intensity, and any hard constraints
# for that day. The slot-level angle from SLOT_CONFIGS is layered on top of this.
CAMPAIGN_DAY_CONFIGS: dict[tuple[int, int], dict[str, str]] = {

    # ── 7-DAY ARC ─────────────────────────────────────────────────────────────
    (7, 1): {
        "phase": "Teaser / Problem Agitation",
        "narrative": (
            "Do NOT mention the product name or make any sales pitch. "
            "Open the reader's eyes to a painful, relatable problem they have right now: "
            "struggling to earn online despite trying multiple things. "
            "Stir frustration. End with a vague but compelling hint that something exists "
            "which changes everything — but don't name it yet."
        ),
        "sell_intensity": "zero — pure curiosity and empathy, no offer",
        "forbidden": "Do not name the product. Do not include a buy link.",
    },
    (7, 2): {
        "phase": "Introduce the Solution",
        "narrative": (
            "Reveal the product by name for the first time — use the exact name from the PRODUCT COPY. "
            "Explain what it is in one punchy sentence drawn from its core promise. "
            "Focus on the headline benefit: what does it let a beginner do that they couldn't before? "
            "Keep it high-level — no deep feature lists yet. "
            "The reader should feel 'this is different from what I've seen before.'"
        ),
        "sell_intensity": "soft — introduce and intrigue, one gentle CTA",
        "forbidden": "Don't oversell. No urgency language yet — the launch hasn't started.",
    },
    (7, 3): {
        "phase": "Deep Dive — Mechanism and Features",
        "narrative": (
            "Go deeper into exactly how the product works. Draw the key features and mechanism "
            "steps directly from the PRODUCT COPY — use the actual feature names and steps "
            "described there. Construct one short, concrete micro-example (a fictional beginner "
            "walking through the steps) to make the mechanism feel tangible and simple. "
            "Make it feel believable, not hype-y."
        ),
        "sell_intensity": "medium — educational with a clear CTA",
        "forbidden": "Avoid urgency — no 'closing soon' or 'bonuses disappear' yet.",
    },
    (7, 4): {
        "phase": "Social Proof and Results",
        "narrative": (
            "Lead with real-feeling results drawn from the proof elements in the PRODUCT COPY "
            "(testimonials, case studies, specific numbers). "
            "Use figures that feel attainable for a beginner — not extreme claims. "
            "Reinforce that this works for people who have no tech skills or big budgets."
        ),
        "sell_intensity": "medium-high — proof-backed direct CTA",
        "forbidden": "Don't fabricate claims not in the PRODUCT COPY. Keep results believable.",
    },
    (7, 5): {
        "phase": "Overcome Objections",
        "narrative": (
            "Address the top 3 objections head-on: 'I'm not technical', "
            "'I've tried things like this before and they didn't work', "
            "'I don't have money to invest in ads or tools'. "
            "Knock each down with a brief, confident rebuttal using the product's features "
            "and guarantees from the PRODUCT COPY. "
            "End by restating the core promise and pushing the reader toward the link."
        ),
        "sell_intensity": "medium-high — objection-busting with a direct CTA",
        "forbidden": "Don't start urgency yet — that begins on Day 6.",
    },
    (7, 6): {
        "phase": "Urgency Begins — Bonuses and Limited Time",
        "narrative": (
            "Shift tone: the window is narrowing. List the specific bonuses from the PRODUCT COPY "
            "that the reader gets only if they act today or tomorrow. "
            "Explain that the launch price is temporary and will rise or close. "
            "Use credible, authentic scarcity — not manufactured fake countdown language. "
            "Remind them of everything they've learned this week."
        ),
        "sell_intensity": "high — urgency-led, list bonuses, strong CTA",
        "forbidden": "Don't say 'this is the last email' — save that for Day 7.",
    },
    (7, 7): {
        "phase": "Hard Close — Final Chance",
        "narrative": (
            "This is the final email. Everything closes tonight. Use a definitive, "
            "respectful tone: 'I promised I'd let you know when the door was closing, "
            "and this is it.' Recap the entire value stack (from the PRODUCT COPY) in 3 bullet points. "
            "State a clear deadline. Make the last line of the email the CTA. "
            "After this email, no more follow-up on this offer."
        ),
        "sell_intensity": "maximum — hard close, final deadline, last-chance CTA",
        "forbidden": "Do not introduce any new angles or features. Recap only.",
    },

    # ── 5-DAY ARC ─────────────────────────────────────────────────────────────
    (5, 1): {
        "phase": "Teaser / Problem Agitation",
        "narrative": (
            "Do NOT mention the product name or make any sales pitch. "
            "Open the reader's eyes to a painful, relatable problem they have right now: "
            "struggling to earn online despite trying multiple things. "
            "Stir frustration. End with a vague but compelling hint that something exists "
            "which changes everything — but don't name it yet."
        ),
        "sell_intensity": "zero — pure curiosity and empathy, no offer",
        "forbidden": "Do not name the product. Do not include a buy link.",
    },
    (5, 2): {
        "phase": "Introduce the Solution + How It Works",
        "narrative": (
            "Reveal the product by name — use the exact name from the PRODUCT COPY. "
            "Explain what it is AND describe how it works using the core features found in the copy. "
            "Construct brief, concrete examples from those features. "
            "Balance overview and depth — the reader should understand it AND want it."
        ),
        "sell_intensity": "medium — educational with a clear CTA",
        "forbidden": "No urgency language yet.",
    },
    (5, 3): {
        "phase": "Social Proof and Objection Handling",
        "narrative": (
            "Combine proof with objection-busting. Lead with believable results from the "
            "PRODUCT COPY (specific numbers, beginner success stories). "
            "Then address the top 2 objections ('not technical', 'tried things before and failed'). "
            "End with a confident push toward the link."
        ),
        "sell_intensity": "medium-high — proof-backed, objection-busted CTA",
        "forbidden": "Don't fabricate claims not in the PRODUCT COPY.",
    },
    (5, 4): {
        "phase": "Urgency Begins — Bonuses and Limited Time",
        "narrative": (
            "Shift tone: the window is narrowing. List the specific bonuses from the PRODUCT COPY. "
            "Explain the launch price is temporary. Use credible scarcity. "
            "Remind the reader of everything covered so far."
        ),
        "sell_intensity": "high — urgency-led, list bonuses, strong CTA",
        "forbidden": "Don't say 'this is the last email' — save that for Day 5.",
    },
    (5, 5): {
        "phase": "Hard Close — Final Chance",
        "narrative": (
            "This is the final email. Everything closes tonight. "
            "Use a definitive, respectful tone: 'I promised I'd let you know when the "
            "door was closing, and this is it.' Recap the value stack from the PRODUCT COPY "
            "in 3 bullets. State a clear deadline. Make the last line the CTA."
        ),
        "sell_intensity": "maximum — hard close, final deadline, last-chance CTA",
        "forbidden": "Do not introduce new angles. Recap only.",
    },
}


def build_prompt(slot: str, settings: Settings) -> str:
    cfg = SLOT_CONFIGS[slot]
    today = date.today().isoformat()
    product_copy = load_product_copy(settings.product_copy_file)
    return f"""\
─── PRODUCT COPY (source of truth for all product details) ───
{product_copy}
─── END PRODUCT COPY ───

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


def build_campaign_prompt(
    slot: str,
    day_num: int,
    total_days: int,
    settings: Settings,
) -> str:
    """Build the user-turn prompt for a campaign email.

    Layers the day-arc context (CAMPAIGN_DAY_CONFIGS) on top of the
    slot-level persuasion angle (SLOT_CONFIGS). The day arc governs what
    narrative stage we are at and how hard to sell. The slot angle governs
    how to open and frame that narrative.

    On zero-sell days (Day 1) the CTA is suppressed regardless of slot angle.
    """
    slot_cfg = SLOT_CONFIGS[slot]
    day_cfg = CAMPAIGN_DAY_CONFIGS[(total_days, day_num)]
    today = date.today().isoformat()
    product_copy = load_product_copy(settings.product_copy_file)

    if day_cfg["sell_intensity"].startswith("zero"):
        effective_cta = (
            "none — do not include any call-to-action or affiliate link in this email"
        )
    else:
        effective_cta = slot_cfg["cta_style"]

    return f"""\
─── PRODUCT COPY (source of truth for all product details) ───
{product_copy}
─── END PRODUCT COPY ───

Today is {today}. You are writing email {day_num} of {total_days} in a {total_days}-day \
promotional campaign sequence. Write the {slot} email for Day {day_num}.

─── CAMPAIGN ARC CONTEXT (governs narrative stage and sell intensity) ───
- Campaign phase    : {day_cfg["phase"]}
- Narrative direction: {day_cfg["narrative"]}
- Sell intensity    : {day_cfg["sell_intensity"]}
- Hard constraint   : {day_cfg["forbidden"]}

─── SLOT CONTEXT (governs opening style and timing tone) ───
- Slot              : {slot} send
- Persuasion angle  : {slot_cfg["angle"]}
- Subject direction : {slot_cfg["subject_direction"]}
- Body direction    : {slot_cfg["body_direction"]}
- Call-to-action    : {effective_cta}

─── SEQUENCE COHERENCE ───
- The reader has already received the previous {day_num - 1} email(s) in this sequence.
- Advance the narrative — do not reset it. Avoid repeating hooks, phrases, or \
subject line structures from earlier emails (you won't see them, so simply ensure \
this email feels fresh and distinct in its opening and angle).

─── SENDER AND AUDIENCE ───
- Sender name (sign-off): {settings.sender_name}
- Target audience       : {settings.audience}
- Affiliate link (href for every CTA, unless CTA is suppressed above): \
{settings.affiliate_link}
"""
