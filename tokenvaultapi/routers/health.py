from datetime import datetime

from fastapi import APIRouter

from tokenvaultapi import __version__
from tokenvaultapi.logger import logger
from tokenvaultapi.schemas.health import HealthcheckResponse

router = APIRouter()


@router.get("/healthcheck", response_model=HealthcheckResponse, tags=["health"])
def healthcheck() -> HealthcheckResponse:
    message = "healthy"
    logger.debug(message)
    return HealthcheckResponse(
        message=message,
        version=__version__,
        time=datetime.now(),
    )
