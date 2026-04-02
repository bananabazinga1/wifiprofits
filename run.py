"""
Daily Affiliate Email Generator — entry point.

Usage:
    python run.py

The scheduler will block and fire three jobs per day at the hours configured
in your .env file (MORNING_HOUR, AFTERNOON_HOUR, EVENING_HOUR).
Generated emails are saved to output/YYYY-MM-DD/ as .html and .txt files.
Press Ctrl+C to stop.
"""

import logging
import sys

from keep_alive import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("email_generator.log", encoding="utf-8"),
    ],
)

# Import config first — triggers .env load and validation.
from email_generator.config import settings  # noqa: E402
from email_generator.scheduler import build_scheduler  # noqa: E402

logger = logging.getLogger(__name__)


def main() -> None:
    keep_alive()
    logger.info("=" * 60)
    logger.info("Daily Affiliate Email Generator starting")
    logger.info("  Model       : %s", settings.claude_model)
    logger.info("  Affiliate   : %s", settings.affiliate_link)
    logger.info("  Sender name : %s", settings.sender_name)
    logger.info(
        "  Schedule    : %02d:00 / %02d:00 / %02d:00 (local time)",
        settings.morning_hour,
        settings.afternoon_hour,
        settings.evening_hour,
    )
    logger.info("  Output dir  : %s/", settings.output_dir)
    logger.info("=" * 60)

    scheduler = build_scheduler()
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
