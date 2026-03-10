import os
from typing import Final

from loguru import logger
from loki_logger_handler.formatters.loguru_formatter import LoguruFormatter
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler

LABELS: Final[dict[str, str]] = {
    "app": "portfolio",
    "env": os.environ.get("PORTFOLIO_ENV", "dev"),
}


log_handler: LokiLoggerHandler = LokiLoggerHandler(
    url=str(os.environ.get("PORTFOLIO_LOKI_URL")).split(),
    labels=LABELS,
    label_keys={"module"},
    timeout=10,
    default_formatter=LoguruFormatter(),
)

logger.configure(handlers=[{"sink": log_handler, "serialize": True}])

__all__ = ["logger"]
