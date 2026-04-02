import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from email_generator.config import settings
from email_generator.generator import generate_email
from email_generator.writer import write_email

logger = logging.getLogger(__name__)


def _make_job(slot: str):
    """Return a callable that generates and saves one email for the given slot."""
    def job():
        logger.info("Generating %s email...", slot)
        try:
            subject, html_body, plain_body = generate_email(slot)
            write_email(slot, subject, html_body, plain_body)
            logger.info("[%s] %s email done — %s", datetime.now().strftime("%H:%M"), slot, subject[:70])
        except Exception:
            logger.exception("Failed to generate %s email", slot)
    job.__name__ = f"generate_{slot}_email"
    return job


def build_scheduler() -> BlockingScheduler:
    jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}
    scheduler = BlockingScheduler(jobstores=jobstores, timezone="local")

    slots = [
        ("morning", settings.morning_hour),
        ("afternoon", settings.afternoon_hour),
        ("evening", settings.evening_hour),
    ]

    for slot, hour in slots:
        scheduler.add_job(
            _make_job(slot),
            trigger=CronTrigger(hour=hour, minute=0),
            id=slot,
            replace_existing=True,
            misfire_grace_time=3600,
        )
        logger.info("Scheduled %s email at %02d:00", slot, hour)

    return scheduler
