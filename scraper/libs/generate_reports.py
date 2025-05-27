import json
from typing import Optional

from google import generativeai

from scraper.configs.constants import (
    AI_MODEL,
    EXTRACTING_PROMPT,
    GEMINI_API_KEY,
    PROMINENT_ANALYSIS_PROMPT,
    RC_ANALYSIS_PROMPT,
    SENTIMENT_ANALYSIS_PROMPT,
)
from scraper.configs.models import ResponseContent, Site
from scraper.libs.logger import setup_logger

logger = setup_logger(__name__)

generativeai.configure(api_key=GEMINI_API_KEY)
model = generativeai.GenerativeModel(AI_MODEL)


async def _generate_analysis(
    url: str,
    analysis_type: str,
    prompt: Optional[str],
    analysis_field: str,
    has_analysis_field: str,
):
    """Generate AI analysis for a given URL"""
    try:
        logger.info(f"Preparing to generate {analysis_type} for {url}")

        if not prompt:
            logger.warning(f"No prompt configured for {analysis_type}")
            return

        response = model.generate_content(f"{prompt} {url}")
        logger.info(f"{analysis_type} generated successfully")

        current_data = await Site.filter(url=url).first()
        if current_data:
            logger.info(f"Saving {analysis_type} to database...")
            setattr(current_data, analysis_field, response.text)
            setattr(current_data, has_analysis_field, True)
            await current_data.save()
            logger.info(f"{analysis_type} saved to database")
        else:
            logger.error("URL not found in database, please check the URL")

    except Exception as e:
        logger.error(f"Error generating {analysis_type}: {e}")
        raise


async def rc_analysis(url: str):
    """Generate Root Cause Analysis"""
    await _generate_analysis(
        url, "Root Cause Analysis", RC_ANALYSIS_PROMPT, "rc_analysis", "has_rc_analysis"
    )


async def sentiment_analysis(url: str):
    """Generate Sentiment Analysis"""
    await _generate_analysis(
        url,
        "Sentiment Analysis",
        SENTIMENT_ANALYSIS_PROMPT,
        "sentiment_analysis",
        "has_sentiment_analysis",
    )


async def prominent_analysis(url: str):
    """Generate Prominent Analysis"""
    await _generate_analysis(
        url,
        "Prominent Analysis",
        PROMINENT_ANALYSIS_PROMPT,
        "prominent_analysis",
        "has_prominent_analysis",
    )


async def extract_content_site(url: str) -> ResponseContent:
    """Extract content from a website URL"""
    response = None
    try:
        logger.info(f"Preparing to extract content for {url}")

        if not EXTRACTING_PROMPT:
            raise ValueError("EXTRACTING_PROMPT not configured")

        logger.info(f"Using prompt: {EXTRACTING_PROMPT[:100]}...")
        response = model.generate_content(f"{EXTRACTING_PROMPT} {url}")
        logger.info("Content extracted successfully")

        # Clean the response text
        cleaned_response = response.text.strip("```json").strip("```").strip()
        logger.debug(f"Cleaned response: {cleaned_response}")

        return ResponseContent(**json.loads(cleaned_response))

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Raw response: {response.text if response else 'No response'}")
        # Return fallback response
        return ResponseContent(content="N/A", title="N/A")
    except Exception as e:
        logger.error(f"Error extracting content from {url}: {e}")
        raise
