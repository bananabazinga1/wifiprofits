"""
generate_campaign.py — Batch-generate a complete promotional email campaign.

Usage:
    python generate_campaign.py --days 5
    python generate_campaign.py --days 7

All emails for the entire campaign are generated in one run and saved to:
    output/campaign_<YYYY-MM-DD>_<N>days/
        day_1/
            email_1_morning.html / .txt
            email_2_afternoon.html / .txt
            email_3_evening.html / .txt
        ...
        day_N/
        campaign_index.txt   ← subject-line summary for every email

API calls are made synchronously. Progress is printed to stdout.
If an individual email fails, generation continues and failures are reported
at the end and recorded in campaign_index.txt.

Press Ctrl+C to abort. Emails already written are preserved.
"""

import argparse
import logging
import sys


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a complete 5-day or 7-day affiliate email campaign upfront.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        choices=[5, 7],
        metavar="{5,7}",
        help="Number of campaign days. Must be 5 or 7.",
    )
    return parser.parse_args()


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("campaign_generator.log", encoding="utf-8"),
        ],
    )


def main() -> None:
    args = _parse_args()
    _configure_logging()

    # Import after logging is set up so any config errors surface cleanly.
    from email_generator.config import settings
    from email_generator.campaign import run_campaign

    total_emails = args.days * 3

    print("=" * 60)
    print("WiFi Profits Campaign Generator")
    print(f"  Campaign    : {args.days}-day ({total_emails} emails total)")
    print(f"  Model       : {settings.claude_model}")
    print(f"  Affiliate   : {settings.affiliate_link}")
    print(f"  Sender name : {settings.sender_name}")
    print(f"  Output dir  : {settings.output_dir}/")
    print("=" * 60)
    print()

    try:
        run_campaign(total_days=args.days)
    except KeyboardInterrupt:
        print("\nAborted. Emails written so far have been preserved.")
        sys.exit(1)
    except Exception:
        logging.getLogger(__name__).exception("Unexpected error during campaign generation.")
        sys.exit(1)


if __name__ == "__main__":
    main()
