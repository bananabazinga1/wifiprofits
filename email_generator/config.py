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
    product_copy_file: str


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
        product_copy_file=os.getenv("PRODUCT_COPY_FILE", "product_copy.txt"),
    )


def load_product_copy(path: str) -> str:
    """Read and return the raw sales-page copy from *path*.

    Raises FileNotFoundError with actionable instructions if the file is absent.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Product copy file not found: {path!r}\n"
            "Create this file and paste your sales page copy into it, or set\n"
            "PRODUCT_COPY_FILE in your .env to point to an existing file.\n"
            "See product_copy_example.txt for the expected format."
        ) from None


settings = _load()
