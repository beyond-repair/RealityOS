"""
RealityOS API Entrypoint
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app import __version__

app = FastAPI(
    title="RealityOS",
    description=(
        "Local in-memory MVP for organizational what-if questions. "
        "Confidence is a heuristic (model_version mvp-heuristic-0.1), "
        "not a calibrated forecast and not an operating system."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # Wildcard origins cannot be paired with credentialed requests.
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/v1")


@app.get("/", tags=["Health"])
def root():
    return {
        "name": "RealityOS",
        "version": __version__,
        "status": "ok",
        "persistence": "in-memory",
        "model_version": "mvp-heuristic-0.1",
        "docs": "/docs",
        "message": "Heuristic what-if API is running. Not a calibrated organizational twin.",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
