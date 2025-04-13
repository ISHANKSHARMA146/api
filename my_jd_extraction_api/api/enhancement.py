from fastapi import APIRouter, HTTPException, Body
import logging

from my_jd_extraction_api.services.jd_enhancement import JobDescriptionEnhancer
from my_jd_extraction_api.schemas.jd_schema import JobDescriptionSchema, JobDescriptionEnhancementResponse

# Initialize Logger
logger = logging.getLogger(__name__)

# Initialize Router
router = APIRouter(
    prefix="/enhancement",
    tags=["enhancement"],
    responses={404: {"description": "Not found"}},
)

# Initialize Service
jd_enhancer = JobDescriptionEnhancer()

@router.post("/", response_model=JobDescriptionEnhancementResponse)
async def enhance_job_description(jd_data: dict = Body(...)):
    """
    Enhance an extracted job description with more detailed information.
    
    Parameters:
    - jd_data: The extracted job description data (typically from the extraction endpoint)
    
    Returns:
    - JobDescriptionEnhancementResponse: Enhanced job description data
    """
    try:
        logger.info("Enhancing job description")
        
        # Validate input
        if not jd_data or "extracted_jd" not in jd_data:
            raise HTTPException(
                status_code=400,
                detail="Invalid input. Expected a dictionary with 'extracted_jd' key."
            )
        
        # Enhance job description
        enhanced_data = await jd_enhancer.enhance_job_description(jd_data["extracted_jd"])
        
        return enhanced_data
        
    except Exception as e:
        logger.error(f"Error enhancing job description: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error enhancing job description: {str(e)}") 