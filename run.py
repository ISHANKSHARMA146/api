"""
Simple script to run the Job Description Extraction & Enhancement API
"""
import uvicorn
import os
from my_jd_extraction_api.api.main import app

# Export app object for Vercel
app = app

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the API - module path directly
    uvicorn.run("my_jd_extraction_api.api.main:app", host="0.0.0.0", port=port, reload=True) 