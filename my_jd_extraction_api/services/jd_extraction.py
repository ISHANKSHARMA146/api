from io import BytesIO
import logging
from typing import Dict, Any
from datetime import datetime
import json

from my_jd_extraction_api.services.file_parser import parse_file
from my_jd_extraction_api.services.gpt_service import GPTService
from my_jd_extraction_api.schemas.jd_schema import JobDescriptionSchema, JobDescriptionExtractionResponse

# Initialize Logger
logger = logging.getLogger(__name__)

class JobDescriptionExtractor:
    """
    Service for extracting structured information from job description files.
    """
    def __init__(self):
        """
        Initialize the JD extraction service.
        """
        self.gpt_service = GPTService()
        logger.info("JobDescriptionExtractor initialized successfully")

    async def extract_job_description(self, file_buffer: BytesIO, filename: str) -> Dict[str, Any]:
        """
        Extract structured job description data from a file.
        
        Args:
            file_buffer: The uploaded file buffer.
            filename: Name of the uploaded file.
            
        Returns:
            Dict containing structured job description data.
        """
        try:
            # Parse file to extract text
            text = parse_file(file_buffer, filename)
            
            # Build prompts for GPT extraction
            system_prompt, user_prompt = self._build_extraction_prompts(text)
            
            # Extract structured data
            structured_data = await self.gpt_service.extract_with_schema(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_schema=JobDescriptionExtractionResponse
            )
            
            # Add original text for reference
            structured_data["extracted_jd"]["original_text"] = text
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Error extracting job description from '{filename}': {str(e)}", exc_info=True)
            raise Exception(f"Error extracting job description: {str(e)}")

    def _build_extraction_prompts(self, text: str) -> tuple:
        """
        Build system and user prompts for GPT extraction.
        
        Args:
            text: Extracted text from the job description file.
            
        Returns:
            Tuple of (system_prompt, user_prompt).
        """
        today_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create a sample of the expected JSON structure
        example_structure = {
            "extracted_jd": {
                "basic_info": {
                    "job_title": "Example Title",
                    "job_code": "ABC123",
                    "job_level": "L5",
                    "department": "Engineering",
                    "job_category": "Software Development"
                },
                "posting_metadata": {
                    "contract_duration": "Permanent",
                    "time_commitment": "Full-time"
                },
                "role_description": {
                    "job_summary": "Example summary",
                    "daily_tasks": ["Task 1", "Task 2"],
                    "performance_indicators": ["KPI 1", "KPI 2"],
                    "decision_making_authority": "Medium",
                    "stakeholder_interactions": ["Stakeholder 1", "Stakeholder 2"]
                }
                # Other sections would be included here
            },
            "message": "Job description extracted successfully"
        }

        # Format the example structure as a pretty JSON string
        example_json = json.dumps(example_structure, indent=2)
        
        system_prompt = f"""
        You are an AI assistant specialized in extracting and inferring information from job descriptions.
        Today's date is {today_date}.
        
        Your task is to extract information from a job description text and structure it according to the specified schema.
        
        IMPORTANT: You MUST follow the EXACT JSON structure shown below. The response must contain an 'extracted_jd' field with nested fields.
        
        Here is an example of the required JSON structure (partial example):
        
        {example_json}
        
        CRITICAL INSTRUCTION: You MUST provide values for ALL fields in the schema. Do not use null values or empty arrays.
        If information is not explicitly stated in the job description:
        - Make reasonable inferences based on the job title, industry context, and similar roles
        - Provide plausible content for every field
        - Use industry standards and common practices to fill gaps
        - For numeric fields like salary, provide realistic ranges based on the role/industry
        - For boolean fields, choose the most likely value based on context
        
        Follow these guidelines for extraction:
        
        1. BASIC JOB INFO (as 'basic_info' field):
           - job_title: Extract the job title
           - job_code: Extract the requisition ID if present, or create a plausible one
           - job_level: Extract internal grading if mentioned, or infer one based on the job title/responsibilities
           - department: Extract department, division, or business unit, or infer from responsibilities
           - job_category: Extract function or job category, or derive from the job title/responsibilities
        
        2. JOB POSTING METADATA (as 'posting_metadata' field):
           - contract_duration: Extract contract duration if mentioned, or infer based on job type
           - time_commitment: Extract time commitment details, or assume typical arrangement for role
        
        3. DETAILED ROLE DESCRIPTION (as 'role_description' field):
           - job_summary: Extract job summary/objective (must be comprehensive, 100+ words)
           - daily_tasks: List at least 10 specific day-to-day tasks as an array of strings
           - performance_indicators: List at least 5 KPIs as an array of strings
           - decision_making_authority: Detail authority level (must provide substantive description)
           - stakeholder_interactions: List at least 5 stakeholder interactions as an array of strings
        
        4. REQUIREMENTS BREAKDOWN (as 'requirements' field):
           - required_qualifications: List at least 5 required qualifications as an array of strings
           - preferred_qualifications: List at least 3 preferred qualifications as an array of strings
           - mandatory_certifications: List relevant certifications as an array of strings
           - legal_eligibility: Provide eligibility requirements (never leave empty)
           - background_checks: Specify typical background check requirements for this kind of role
           - clearance_level: Specify appropriate clearance level based on the role
        
        5. SKILLS CLASSIFICATION (as 'skills' field):
           - hard_skills: List at least 8 hard skills as an array of strings
           - soft_skills: List at least 5 soft skills as an array of strings
           - domain_expertise: List at least 3 domain expertise areas as an array of strings
           - methodologies: List at least 3 methodologies as an array of strings
           - languages: List relevant language skills as an array of strings
           - skills_priority: Categorize skills by priority (must-have vs. nice-to-have) as object with arrays
        
        6. COMPENSATION DETAILS (as 'compensation' field):
           - base_salary: Provide realistic salary range for the role and industry
           - bonus_structure: Describe typical bonus/commission structure for similar roles
           - equity: Describe typical equity/stock options if applicable to the industry/role
           - benefits: List at least 5 benefits as an array of strings
           - relocation_assistance: Specify whether relocation assistance is likely available (true/false)
           - visa_sponsorship: Specify whether visa sponsorship is likely available (true/false)
        
        7. WORK ENVIRONMENT (as 'work_environment' field):
           - work_model: Specify work model (remote, hybrid, on-site)
           - locations: List at least one work location as an array of strings
           - travel_requirements: Specify travel expectations
           - shift_type: Specify shift type arrangement
        
        8. CAREER PATH INFO (as 'career_path' field):
           - growth_opportunities: Describe potential career progression paths
           - training_programs: List at least 3 typical training programs as an array of strings
           - mentorship: Describe mentorship opportunities
           - succession_planning: Describe succession planning process
           - culture_page_link: Provide placeholder or realistic URL
           - careers_page_link: Provide placeholder or realistic URL
        
        IMPORTANT: DO NOT leave any field empty, null, or with an empty array. Infer reasonable values for ALL fields.
        REMEMBER: Your response MUST match the expected schema format with 'extracted_jd' as the top-level key.
        """
        
        user_prompt = f"""
        Extract and infer structured information from the following job description:
        
        {text}
        
        Format the output according to the specified schema with all relevant sections.
        The response MUST include the 'extracted_jd' field as the top-level key.
        Remember to COMPLETELY FILL IN every field with substantive content - do not leave any field empty or null.
        Use reasonable inferences based on the job context for any missing information.
        """
        
        return system_prompt, user_prompt 