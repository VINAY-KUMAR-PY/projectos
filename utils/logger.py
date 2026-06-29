from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

logger.add(
    "outputs/projectos.log",
    rotation="10 MB",
    retention="30 days",
    level="DEBUG"
)

app_logger = logger