from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path for proper imports when running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from my_jd_extraction_api.api.extraction import router as extraction_router
from my_jd_extraction_api.api.enhancement import router as enhancement_router
from my_jd_extraction_api.api.combined import router as combined_router
from my_jd_extraction_api.config.settings import get_settings

# Initialize Settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Initialize FastAPI App
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {
        "message": "Job Description Extraction & Enhancement API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

# Include routers
app.include_router(extraction_router)
app.include_router(enhancement_router)
app.include_router(combined_router)

# For local development
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run with the module path for proper imports
    uvicorn.run("my_jd_extraction_api.api.main:app", host="0.0.0.0", port=port, reload=True) 