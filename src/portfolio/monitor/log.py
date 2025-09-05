import os
from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
from loki_logger_handler.formatters.loguru_formatter import LoguruFormatter
from loguru import logger

log_handler = LokiLoggerHandler(
    url=os.environ.get("LOKI_URL"),
    labels={"app": "portfolio"},
    label_keys={},
    timeout=10,
    default_formatter=LoguruFormatter(),
)

logger.configure(handlers=[{"sink": log_handler, "serialize": True}])
