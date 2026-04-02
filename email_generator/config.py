import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str
    affiliate_link: str
    sender_name: str
    audience: str
    morning_hour: int
    afternoon_hour: int
    evening_hour: int
    output_dir: str
    claude_model: str


def _load() -> Settings:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY is not set. "
            "Copy .env.example to .env and add your Anthropic API key."
        )
    return Settings(
        api_key=api_key,
        affiliate_link=os.getenv(
            "AFFILIATE_LINK", "https://warriorplus.com/o2/a/YOURLINK/0"
        ),
        sender_name=os.getenv("SENDER_NAME", "Your Name"),
        audience=os.getenv("AUDIENCE", "online business beginners"),
        morning_hour=int(os.getenv("MORNING_HOUR", "8")),
        afternoon_hour=int(os.getenv("AFTERNOON_HOUR", "13")),
        evening_hour=int(os.getenv("EVENING_HOUR", "19")),
        output_dir=os.getenv("OUTPUT_DIR", "output"),
        claude_model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5"),
    )


settings = _load()
