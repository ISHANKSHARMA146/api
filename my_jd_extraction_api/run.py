"""
Simple script to run the Job Description Extraction & Enhancement API
"""
import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the API
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True, 
                app_dir="my_jd_extraction_api") 