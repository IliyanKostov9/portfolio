import os
from typing import Final
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from loki_logger_handler.formatters.loguru_formatter import LoguruFormatter
from loguru import logger


LABELS: Final[dict[str, str]] = {"app": "portfolio"}


log_handler: LokiLoggerHandler = LokiLoggerHandler(
    url=os.environ.get("PORTFOLIO_LOKI_URL"),
    labels=LABELS,
    label_keys={"module"},
    timeout=10,
    default_formatter=LoguruFormatter(),
)

logger.configure(handlers=[{"sink": log_handler, "serialize": True}])

__all__ = ["logger"]
