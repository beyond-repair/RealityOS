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
        "Autonomous Decision Infrastructure. "
        "Living organizational simulations that answer ‘What happens if…?’ "
        "with calibrated confidence and full provenance."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/v1")


@app.get("/", tags=["Health"])
def root():
    return {
        "name": "RealityOS",
        "version": __version__,
        "status": "live",
        "docs": "/docs",
        "message": "Decision infrastructure is online.",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
