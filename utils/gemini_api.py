import os
from dotenv import load_dotenv
import json
import logging
from typing import Dict, Optional, Any
import google.generativeai as genai
import requests

# Configure logging
logger = logging.getLogger(__name__)

# Configure the Gemini API with API key from environment variables
API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Initialize Gemini if API key is available
try:
    if API_KEY:
        genai.configure(api_key=API_KEY)
    else:
        logger.warning("GEMINI_API_KEY environment variable not set")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")

def analyze_symptoms(context: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Analyze symptoms using Gemini AI and return potential conditions.
    
    Args:
        context: Dictionary containing symptoms and optional information like age and gender
        
    Returns:
        Dictionary containing analysis results or None if an error occurs
    """
    try:
        if not API_KEY:
            logger.error("Cannot analyze symptoms: GEMINI_API_KEY is not set")
            return None
        
        # Extract information from context
        symptoms = context.get("symptoms", "")
        age = context.get("age", "")
        gender = context.get("gender", "")
        
        # Create a prompt for the Gemini model
        prompt = f"""
        You are a medical symptoms analyzer. Based on the symptoms provided, suggest possible 
        medical conditions. For each condition, provide a brief description and common symptoms.
        Also suggest if the user should seek immediate medical attention, visit a doctor soon, 
        or if the condition may resolve on its own with home care.
        
        DO NOT diagnose the user. Make it clear these are only possibilities based on limited 
        information. Return your response as a JSON object with the following structure:
        {{
            "possible_conditions": [
                {{
                    "name": "Condition name",
                    "description": "Brief description",
                    "common_symptoms": ["symptom1", "symptom2", ...],
                    "urgency_level": "immediate_attention|doctor_visit|self_care"
                }},
                ...
            ],
            "disclaimer": "Medical disclaimer text",
            "general_advice": "General health advice"
        }}
        
        User symptoms: {symptoms}
        {"User age: " + age if age else ""}
        {"User gender: " + gender if gender else ""}
        """
        
        # Generate response using Gemini model
        # Try with the newer model name format first
        try:
            model = genai.GenerativeModel('models/gemini-1.5-pro')
            response = model.generate_content(prompt)
        except Exception as model_error:
            logger.error(f"Model generation failed: {model_error}")
            # Fall back to the older model name format
            logger.debug(f"First model attempt failed: {str(model_error)}, trying fallback model")
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
            except Exception as fallback_error:
                logger.error(f"Fallback model generation failed: {fallback_error}")
                # As a last resort, try gemini-1.0-pro
                logger.debug(f"Second model attempt failed: {str(fallback_error)}, trying last fallback model")
                model = genai.GenerativeModel('gemini-1.0-pro')
                response = model.generate_content(prompt)
        
        # Process the response
        if response and response.text:
            # Extract JSON from response
            try:
                # Sometimes the API returns the JSON string with markdown code blocks
                text = response.text
                if "```json" in text:
                    # Extract content between json code blocks
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    # Extract content between generic code blocks
                    text = text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(text)
                return result
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from Gemini response: {e}")
                logger.debug(f"Raw response: {response.text}")
                
                # Attempt to structure the response manually
                return {
                    "possible_conditions": [],
                    "raw_response": response.text,
                    "disclaimer": "IMPORTANT: This information is not a diagnosis. Always consult with a healthcare professional about your symptoms.",
                    "general_advice": "Please seek medical attention if you're concerned about your symptoms."
                }
        
        return None
    
    except Exception as e:
        logger.error(f"Error in analyze_symptoms: {str(e)}")
        return None
