import os
import logging
from datetime import datetime

from email_generator.config import settings
from email_generator.prompts import SLOT_NUMBER

logger = logging.getLogger(__name__)

HTML_SKELETON = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #222;">
<!-- Generated: {timestamp} | Slot: {slot} | Subject: {subject} -->
{html_body}
</body>
</html>
"""

PLAIN_HEADER = "Generated: {timestamp} | Slot: {slot} | Subject: {subject}\n{separator}\n\n"


def write_email(slot: str, subject: str, html_body: str, plain_body: str) -> None:
    """Write the generated email to disk as .html and .txt files."""
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    number = SLOT_NUMBER.get(slot, 0)

    out_dir = os.path.join(settings.output_dir, today)
    os.makedirs(out_dir, exist_ok=True)

    base_name = f"email_{number}_{slot}"
    html_path = os.path.join(out_dir, f"{base_name}.html")
    txt_path = os.path.join(out_dir, f"{base_name}.txt")

    html_content = HTML_SKELETON.format(
        subject=subject,
        timestamp=timestamp,
        slot=slot,
        html_body=html_body,
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    plain_content = (
        PLAIN_HEADER.format(
            timestamp=timestamp,
            slot=slot,
            subject=subject,
            separator="-" * 60,
        )
        + plain_body
    )
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_content)

    logger.info("Saved: %s  |  %s", html_path, txt_path)


def write_campaign_email(
    slot: str,
    day_num: int,
    subject: str,
    html_body: str,
    plain_body: str,
    campaign_dir: str,
) -> tuple[str, str]:
    """Write one campaign email under a pre-constructed campaign directory.

    Directory layout:
        <campaign_dir>/day_<N>/email_<slot_num>_<slot>.html
        <campaign_dir>/day_<N>/email_<slot_num>_<slot>.txt

    The campaign_dir path is computed once by the caller (campaign.py) so the
    output root stays stable across all API calls regardless of clock drift.

    Returns (html_path, txt_path) so the caller can record them in the index.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    number = SLOT_NUMBER.get(slot, 0)

    day_dir = os.path.join(campaign_dir, f"day_{day_num}")
    os.makedirs(day_dir, exist_ok=True)

    base_name = f"email_{number}_{slot}"
    html_path = os.path.join(day_dir, f"{base_name}.html")
    txt_path = os.path.join(day_dir, f"{base_name}.txt")

    html_content = HTML_SKELETON.format(
        subject=subject,
        timestamp=timestamp,
        slot=slot,
        html_body=html_body,
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    plain_content = (
        PLAIN_HEADER.format(
            timestamp=timestamp,
            slot=slot,
            subject=subject,
            separator="-" * 60,
        )
        + plain_body
    )
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plain_content)

    logger.info("Saved: %s  |  %s", html_path, txt_path)
    return html_path, txt_path
