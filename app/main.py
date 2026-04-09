from fastapi import FastAPI

from .core.config import setup_cors
from .routers.routes import api_router


app = FastAPI(
    title="VDZPlayer API",
    description="API of VDZPlayer that can be used for processing videos and thumbnails.",
    version="1.0.0"
)

setup_cors(app)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Subscription Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
