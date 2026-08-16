import os
from typing import Final


def configure() -> None:
    ENV: Final[str] = os.environ.get("PORTFOLIO_ENV", "dev")
    if ENV == "dev":
        from dotenv import load_dotenv

        load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.models.settings.env")
    os.environ.setdefault("DJANGO_CONFIGURATION", ENV.capitalize())
