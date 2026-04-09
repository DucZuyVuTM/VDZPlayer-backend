import os
from fastapi.middleware.cors import CORSMiddleware


PRODUCTION_ORIGIN = os.getenv("PRODUCTION_ORIGIN", "http://localhost:5173")

origins = [
    PRODUCTION_ORIGIN
]

# CORS middleware
def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
