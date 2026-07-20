from fastapi import FastAPI

from app.api import router as analysis_router


app = FastAPI(
    title="Seshat API",
    version="0.1.0",
)

app.include_router(analysis_router)


@app.get("/")
def health_check() -> dict:
    return {
        "status": "ok",
        "name": "Seshat API",
    }
