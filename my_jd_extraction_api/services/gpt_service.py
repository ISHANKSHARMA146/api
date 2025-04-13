from openai import OpenAI
import logging
from typing import Dict, Any, Type
from pydantic import BaseModel
import json

from my_jd_extraction_api.config.settings import get_settings

# Initialize Logger
logger = logging.getLogger(__name__)

class GPTService:
    """
    Service for interacting with OpenAI's GPT API to extract and enhance job descriptions.
    """
    def __init__(self):
        """
        Initializes the GPT service with the OpenAI API key from settings.
        """
        try:
            settings = get_settings()
            # Initialize OpenAI client with simplified parameters to prevent proxy errors
            self.openai_client = OpenAI(
                api_key=settings.OPENAI_API_KEY
            )
            self.model = settings.GPT_MODEL
            logger.info(f"GPT service initialized successfully with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize GPT service: {str(e)}", exc_info=True)
            raise

    async def extract_with_schema(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Type[BaseModel]
    ) -> Dict[str, Any]:
        """
        Extract structured information using GPT with custom prompts and schema.
        
        Args:
            system_prompt: System-level instructions for GPT.
            user_prompt: User-specific query for GPT processing.
            response_schema: Expected Pydantic schema class for the response.

        Returns:
            Dict containing extracted structured information.
        """
        try:
            # Add required "json" word to system prompt for JSON response format
            if not "json" in system_prompt.lower():
                system_prompt += "\nPlease format your response as JSON."
                
            # Construct the messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            # Make GPT API call
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )

            # Get the response content
            response_content = response.choices[0].message.content
            
            # Parse with Pydantic v2 schema
            parsed_response = response_schema.model_validate_json(response_content)
            
            # Use model_dump instead of dict() in Pydantic v2
            return parsed_response.model_dump()

        except Exception as e:
            logger.error(f"GPT extraction failed: {str(e)}", exc_info=True)
            raise Exception(f"GPT extraction failed: {str(e)}") 