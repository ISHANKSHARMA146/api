from fastapi import APIRouter, HTTPException, UploadFile, File
from io import BytesIO
import logging

from my_jd_extraction_api.services.jd_extraction import JobDescriptionExtractor
from my_jd_extraction_api.schemas.jd_schema import JobDescriptionExtractionResponse

# Initialize Logger
logger = logging.getLogger(__name__)

# Initialize Router
router = APIRouter(
    prefix="/extraction",
    tags=["extraction"],
    responses={404: {"description": "Not found"}},
)

# Initialize Service
jd_extractor = JobDescriptionExtractor()

@router.post("/", response_model=JobDescriptionExtractionResponse)
async def extract_job_description(file: UploadFile = File(...)):
    """
    Extract structured information from a job description file.
    
    Parameters:
    - file: The job description file (PDF, DOCX, or image)
    
    Returns:
    - JobDescriptionExtractionResponse: Structured job description data
    """
    try:
        logger.info(f"Extracting job description from file: {file.filename}")
        
        # Read file contents
        file_buffer = BytesIO(await file.read())
        
        # Extract job description
        extracted_data = await jd_extractor.extract_job_description(file_buffer, file.filename)
        
        return extracted_data
        
    except Exception as e:
        logger.error(f"Error extracting job description: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error extracting job description: {str(e)}") 