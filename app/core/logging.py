import logging
import sys
from app.core.config import settings


def setup_logging() -> None:
    """
    Configures structured application-wide logging.
    Formats logs with timestamps, levels, file lines, and messages.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    log_format = (
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"
    )

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )

    # Reduce noisy logs from external dependencies
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)


# Reusable logger instance for the application
logger = logging.getLogger("paycore")
