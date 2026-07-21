from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Check API health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "seshat-api",
    }
