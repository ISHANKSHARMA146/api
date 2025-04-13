from fastapi import APIRouter, HTTPException, UploadFile, File
from io import BytesIO
import logging

from my_jd_extraction_api.services.jd_extraction import JobDescriptionExtractor
from my_jd_extraction_api.services.jd_enhancement import JobDescriptionEnhancer
from my_jd_extraction_api.schemas.jd_schema import JobDescriptionEnhancementResponse

# Initialize Logger
logger = logging.getLogger(__name__)

# Initialize Router
router = APIRouter(
    prefix="/process",
    tags=["process"],
    responses={404: {"description": "Not found"}},
)

# Initialize Services
jd_extractor = JobDescriptionExtractor()
jd_enhancer = JobDescriptionEnhancer()

@router.post("/", response_model=JobDescriptionEnhancementResponse)
async def extract_and_enhance_job_description(file: UploadFile = File(...)):
    """
    Extracts job description data from a file and immediately enhances it in one API call.
    
    Parameters:
    - file: The job description file (PDF, DOCX, or image)
    
    Returns:
    - JobDescriptionEnhancementResponse: Enhanced job description data
    """
    try:
        logger.info(f"Processing job description from file: {file.filename}")
        
        # Read file contents
        file_buffer = BytesIO(await file.read())
        
        # Step 1: Extract job description
        logger.info("Extracting job description data")
        extracted_data = await jd_extractor.extract_job_description(file_buffer, file.filename)
        
        # Step 2: Enhance the extracted job description
        logger.info("Enhancing extracted job description data")
        enhanced_data = await jd_enhancer.enhance_job_description(extracted_data["extracted_jd"])
        
        logger.info("Successfully processed job description")
        return enhanced_data
        
    except Exception as e:
        logger.error(f"Error processing job description: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing job description: {str(e)}") 