from typing import NoReturn

from fastapi import HTTPException, status


def database_not_configured(resource: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"The {resource} database service is not configured yet.",
    )
