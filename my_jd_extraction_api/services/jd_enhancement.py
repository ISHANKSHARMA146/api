import logging
from typing import Dict, Any
import json

from my_jd_extraction_api.services.gpt_service import GPTService
from my_jd_extraction_api.schemas.jd_schema import JobDescriptionSchema, JobDescriptionEnhancementResponse

# Initialize Logger
logger = logging.getLogger(__name__)

class JobDescriptionEnhancer:
    """
    Service for enhancing extracted job descriptions with more detailed information.
    """
    def __init__(self):
        """
        Initialize the JD enhancement service.
        """
        self.gpt_service = GPTService()
        logger.info("JobDescriptionEnhancer initialized successfully")

    async def enhance_job_description(self, extracted_jd: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance an extracted job description with more detailed information.
        
        Args:
            extracted_jd: The extracted job description data.
            
        Returns:
            Dict containing enhanced job description data.
        """
        try:
            # Build prompts for GPT enhancement
            system_prompt, user_prompt = self._build_enhancement_prompts(extracted_jd)
            
            # Enhance the job description
            enhanced_data = await self.gpt_service.extract_with_schema(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_schema=JobDescriptionEnhancementResponse
            )
            
            # Preserve the original text
            if "original_text" in extracted_jd:
                enhanced_data["enhanced_jd"]["original_text"] = extracted_jd["original_text"]
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error enhancing job description: {str(e)}", exc_info=True)
            
            # If there's a validation error involving boolean fields, attempt to fix it
            if "bool_parsing" in str(e):
                try:
                    logger.info("Attempting to fix boolean field validation errors")
                    # Try to recover by using a post-processing function
                    enhanced_data = self._process_enhancement_with_bool_fix(extracted_jd)
                    return enhanced_data
                except Exception as fix_error:
                    logger.error(f"Error fixing boolean fields: {str(fix_error)}", exc_info=True)
                    
            raise Exception(f"Error enhancing job description: {str(e)}")
            
    async def _process_enhancement_with_bool_fix(self, extracted_jd: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process enhancement with special handling for boolean fields.
        
        Args:
            extracted_jd: The extracted job description data.
            
        Returns:
            Dict containing enhanced job description data with corrected boolean fields.
        """
        system_prompt = """
        You are an AI assistant specialized in creating comprehensive, detailed job descriptions.
        
        Your task is to take an extracted job description and transform it into a professional, detailed job posting.
        
        EXTREMELY IMPORTANT: For the fields 'relocation_assistance' and 'visa_sponsorship', you MUST ONLY use true or false (boolean values).
        DO NOT provide text descriptions for these fields. Only use the literal values 'true' or 'false'.
        
        Your output must be valid JSON with the exact structure shown in the example.
        """
        
        user_prompt = f"""
        Create a comprehensive, professional enhancement of the following job description.
        The structure must match the input exactly, and ALL boolean fields must use only true or false values, not text descriptions.
        
        Here is the job description to enhance:
        {json.dumps(extracted_jd, indent=2)}
        
        IMPORTANT REMINDER:
        - 'relocation_assistance' must be either true or false (a boolean value)
        - 'visa_sponsorship' must be either true or false (a boolean value)
        - DO NOT use text descriptions for these fields
        """
        
        # Enhance the job description with special boolean handling
        enhanced_data = await self.gpt_service.extract_with_schema(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_schema=JobDescriptionEnhancementResponse
        )
        
        # Preserve the original text
        if "original_text" in extracted_jd:
            enhanced_data["enhanced_jd"]["original_text"] = extracted_jd["original_text"]
        
        return enhanced_data

    def _build_enhancement_prompts(self, extracted_jd: Dict[str, Any]) -> tuple:
        """
        Build system and user prompts for GPT enhancement.
        
        Args:
            extracted_jd: The extracted job description data.
            
        Returns:
            Tuple of (system_prompt, user_prompt).
        """
        # Convert extracted_jd to a formatted JSON string for the prompt
        jd_json = json.dumps(extracted_jd, indent=2)
        
        # Create a sample of the expected JSON structure with proper Python booleans
        example_structure = {
            "enhanced_jd": {
                "basic_info": {
                    "job_title": "Senior Software Engineer",
                    "job_code": "ABC123",
                    "job_level": "L5",
                    "department": "Engineering",
                    "job_category": "Software Development"
                },
                "posting_metadata": {
                    "contract_duration": "Permanent",
                    "time_commitment": "Full-time"
                },
                "compensation": {
                    "base_salary": "$120,000 - $150,000",
                    "bonus_structure": "Annual bonus up to 15%",
                    "equity": "Stock options available",
                    "benefits": ["Health insurance", "401(k) match", "Paid time off"],
                    "relocation_assistance": True,  # Using Python's True instead of JSON true
                    "visa_sponsorship": False       # Using Python's False instead of JSON false
                },
                # Other sections would be included here
            },
            "message": "Job description enhanced successfully"
        }

        # Format the example structure as a pretty JSON string
        example_json = json.dumps(example_structure, indent=2)
        
        system_prompt = """
        You are an AI assistant specialized in creating comprehensive, detailed job descriptions.
        
        Your task is to take an extracted job description and transform it into a professional, detailed, and comprehensive job posting that would attract top candidates.
        
        IMPORTANT: You MUST follow the EXACT JSON structure shown below. The response must contain an 'enhanced_jd' field with nested fields matching the input structure.
        
        EXTREMELY IMPORTANT: For the fields 'relocation_assistance' and 'visa_sponsorship', you MUST ONLY use true or false (boolean values).
        DO NOT provide text descriptions for these fields. Use only the literal values true or false.
        
        Here is an example of the required JSON structure (partial example):
        
        """ + example_json + """
        
        CRITICAL REQUIREMENT: You MUST provide extensive, detailed values for EVERY SINGLE field. No field should be left empty, null, or with minimal content:
        
        1. DETAILED ROLE DESCRIPTION:
           - job_summary: Create a comprehensive, compelling 300-500 word summary that thoroughly explains the role, its importance, and its impact
           - daily_tasks: List at least 15 specific, detailed day-to-day tasks with clear action verbs and context
           - performance_indicators: Provide at least 8 specific, measurable KPIs that would indicate success in the role
           - decision_making_authority: Write a detailed paragraph (100+ words) on decision-making scope and authority
           - stakeholder_interactions: List at least 10 stakeholder interactions with specifics about frequency and purpose
        
        2. REQUIREMENTS BREAKDOWN:
           - required_qualifications: Expand to at least 10 detailed required qualifications with specific years of experience
           - preferred_qualifications: List at least 8 preferred qualifications with explanations of why they're valuable
           - mandatory_certifications: Provide at least 3 relevant certifications with explanations of their importance
           - legal_eligibility: Create a detailed paragraph on legal requirements (100+ words)
           - background_checks: Specify comprehensive background check details (75+ words)
           - clearance_level: Detail security clearance requirements (75+ words)
        
        3. SKILLS CLASSIFICATION:
           - hard_skills: List at least 15 specific hard skills with proficiency levels
           - soft_skills: List at least 10 soft skills with descriptions of how they apply to the role
           - domain_expertise: List at least 5 domain expertise areas with depth of knowledge required
           - methodologies: List at least 5 methodologies with explanations of how they're used in the role
           - languages: List all relevant programming, human, or domain-specific languages with proficiency levels
           - skills_priority: Organize all skills into must-have and nice-to-have categories with at least 10 in each
        
        4. COMPENSATION DETAILS:
           - base_salary: Provide detailed salary information with range and factors affecting placement
           - bonus_structure: Create a comprehensive bonus structure with percentages and criteria
           - equity: Detail equity compensation with vesting schedule if applicable
           - benefits: List at least 15 benefits with detailed descriptions
           - relocation_assistance: Use ONLY true or false (boolean value)
           - visa_sponsorship: Use ONLY true or false (boolean value)
        
        5. WORK ENVIRONMENT:
           - work_model: Provide detailed information on remote/hybrid/onsite arrangements (100+ words)
           - locations: List all possible work locations with details about each office
           - travel_requirements: Specify detailed travel expectations including frequency, duration, and purposes
           - shift_type: Provide comprehensive information about working hours and schedule flexibility
        
        6. CAREER PATH INFO:
           - growth_opportunities: Write a detailed section (200+ words) on career advancement paths
           - training_programs: List at least 8 specific training programs with descriptions
           - mentorship: Provide extensive details on mentorship opportunities (150+ words)
           - succession_planning: Describe in detail the succession planning process (150+ words)
           - culture_page_link: Provide a realistic URL with description
           - careers_page_link: Provide a realistic URL with description
        
        7. GENERAL IMPROVEMENTS:
           - Use industry-specific terminology and buzzwords to make the JD look authentic
           - Add details that would appeal to top candidates
           - Use compelling language that sells the opportunity
           - Ensure content is consistent with the company and role seniority level
           - Make the job sound challenging but achievable for qualified candidates
        
        REMEMBER:
        1. Do NOT contradict factual information from the original job description
        2. Your response MUST match the expected schema format with 'enhanced_jd' as the top-level key
        3. EVERY field must be EXTENSIVELY filled with detailed, high-quality content
        4. The enhanced job description should be impressive enough to attract top talent
        5. The fields 'relocation_assistance' and 'visa_sponsorship' MUST be boolean (true or false) values, not text
        """
        
        user_prompt = f"""
        Create a comprehensive, professional enhancement of the following job description:
        
        {jd_json}
        
        Return the enhanced job description according to the specified schema.
        The response MUST include the 'enhanced_jd' field as the top-level key.
        
        CRITICAL: Fill EVERY SINGLE FIELD with extensive, detailed content - this enhanced job description must be thorough and comprehensive with NO gaps or minimal fields.
        
        EXTREMELY IMPORTANT REMINDER:
        - The fields 'relocation_assistance' and 'visa_sponsorship' MUST be boolean values (true or false)
        - DO NOT provide text descriptions for these fields - use only true or false
        """
        
        return system_prompt, user_prompt 