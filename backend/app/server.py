from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router


app = FastAPI(
    title="Seshat API",
    description="Story analysis and continuity tracking API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.49.84.45:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "name": "Seshat API",
        "status": "running",
        "documentation": "/docs",
    }
