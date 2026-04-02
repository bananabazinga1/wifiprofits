"""
email_generator/campaign.py

Orchestrates batch generation of all emails for a multi-day promotional campaign.
Called by generate_campaign.py; has no dependency on APScheduler or run.py.
"""

import logging
import os
from dataclasses import dataclass
from datetime import date

from email_generator.config import settings
from email_generator.generator import generate_campaign_email
from email_generator.writer import write_campaign_email

logger = logging.getLogger(__name__)

SLOTS_IN_ORDER = ["morning", "afternoon", "evening"]
_SLOT_NUMBER = {"morning": 1, "afternoon": 2, "evening": 3}


@dataclass
class _EmailRecord:
    day_num: int
    slot: str
    subject: str
    html_path: str
    txt_path: str


@dataclass
class _FailureRecord:
    day_num: int
    slot: str
    error: str


def run_campaign(total_days: int) -> None:
    """Generate all (total_days × 3) campaign emails and write them to disk.

    Args:
        total_days: 5 or 7

    Raises:
        ValueError: if total_days is not 5 or 7
    """
    if total_days not in (5, 7):
        raise ValueError(f"total_days must be 5 or 7, got {total_days}")

    start_date = date.today().isoformat()
    campaign_dir = os.path.join(
        settings.output_dir, f"campaign_{start_date}_{total_days}days"
    )
    os.makedirs(campaign_dir, exist_ok=True)

    total_emails = total_days * len(SLOTS_IN_ORDER)
    counter = 0
    records: list[_EmailRecord] = []
    failures: list[_FailureRecord] = []

    for day_num in range(1, total_days + 1):
        for slot in SLOTS_IN_ORDER:
            counter += 1
            print(f"[{counter}/{total_emails}] Day {day_num} {slot}...", end=" ", flush=True)

            try:
                subject, html_body, plain_body = generate_campaign_email(
                    slot=slot,
                    day_num=day_num,
                    total_days=total_days,
                )
                html_path, txt_path = write_campaign_email(
                    slot=slot,
                    day_num=day_num,
                    subject=subject,
                    html_body=html_body,
                    plain_body=plain_body,
                    campaign_dir=campaign_dir,
                )
                records.append(_EmailRecord(day_num, slot, subject, html_path, txt_path))
                print("done")

            except Exception as exc:
                error_msg = str(exc)
                logger.exception("Failed — Day %d %s: %s", day_num, slot, error_msg)
                failures.append(_FailureRecord(day_num, slot, error_msg))
                print(f"FAILED ({error_msg[:80]})")

    _write_index(campaign_dir, total_days, start_date, records, failures)

    succeeded = len(records)
    failed = len(failures)
    print()
    print(f"Campaign complete: {succeeded}/{total_emails} emails generated.")
    print(f"Output directory : {campaign_dir}/")
    if failures:
        print(f"\nFailed emails ({failed}):")
        for fail in failures:
            print(f"  Day {fail.day_num} {fail.slot}: {fail.error[:100]}")
    else:
        print("All emails generated successfully.")


def _write_index(
    campaign_dir: str,
    total_days: int,
    start_date: str,
    records: list[_EmailRecord],
    failures: list[_FailureRecord],
) -> None:
    """Write campaign_index.txt summarising all subject lines and any failures."""
    index_path = os.path.join(campaign_dir, "campaign_index.txt")

    lines = [
        "CAMPAIGN INDEX",
        f"Generated : {date.today().isoformat()}",
        f"Duration  : {total_days} days",
        f"Start date: {start_date}",
        f"Total emails: {total_days * 3}  |  Generated: {len(records)}  |  Failed: {len(failures)}",
        "",
        "-" * 70,
        "",
    ]

    by_day: dict[int, list[_EmailRecord]] = {}
    for rec in records:
        by_day.setdefault(rec.day_num, []).append(rec)

    for day_num in range(1, total_days + 1):
        lines.append(f"DAY {day_num}")
        day_records = by_day.get(day_num, [])
        for slot in SLOTS_IN_ORDER:
            matched = next((r for r in day_records if r.slot == slot), None)
            if matched:
                num = _SLOT_NUMBER[slot]
                lines.append(f"  [{num}] {slot:<10} | {matched.subject}")
            else:
                fail = next(
                    (f for f in failures if f.day_num == day_num and f.slot == slot),
                    None,
                )
                err_note = f" (error: {fail.error[:60]})" if fail else " (missing)"
                lines.append(f"  [?] {slot:<10} | FAILED{err_note}")
        lines.append("")

    if failures:
        lines.append("-" * 70)
        lines.append("FAILED EMAILS — regenerate these manually:")
        for fail in failures:
            lines.append(f"  Day {fail.day_num} {fail.slot}: {fail.error}")
        lines.append("")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info("Campaign index written: %s", index_path)
