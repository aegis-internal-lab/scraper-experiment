import asyncio
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
from scraper.services.interfaces import AnalysisServiceInterface

logger = setup_logger(__name__)

generativeai.configure(api_key=GEMINI_API_KEY)
model = generativeai.GenerativeModel(AI_MODEL)


class AnalysisService(AnalysisServiceInterface):
    """Service for handling AI analysis operations"""

    async def _generate_analysis(
        self,
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

    async def generate_root_cause_analysis(self, url: str) -> None:
        """Generate root cause analysis for given URL"""
        await self._generate_analysis(
            url, "Root Cause Analysis", RC_ANALYSIS_PROMPT, "rc_analysis", "has_rc_analysis"
        )

    async def generate_sentiment_analysis(self, url: str) -> None:
        """Generate sentiment analysis for given URL"""
        await self._generate_analysis(
            url,
            "Sentiment Analysis",
            SENTIMENT_ANALYSIS_PROMPT,
            "sentiment_analysis",
            "has_sentiment_analysis",
        )

    async def generate_prominent_analysis(self, url: str) -> None:
        """Generate prominent analysis for given URL"""
        await self._generate_analysis(
            url,
            "Prominent Analysis",
            PROMINENT_ANALYSIS_PROMPT,
            "prominent_analysis",
            "has_prominent_analysis",
        )

    async def generate_all_analysis(self, url: str) -> Optional[dict]:
        """Generate all types of analysis for given URL"""
        # Run all analysis in parallel for better performance
        await asyncio.gather(
            self.generate_root_cause_analysis(url),
            self.generate_sentiment_analysis(url),
            self.generate_prominent_analysis(url),
        )

        # Get the updated data
        current_data = await Site.filter(url=url).first()
        if current_data:
            return {
                "url": current_data.url,
                "masked_url": current_data.masked_url,
                "rc_analysis": current_data.rc_analysis,
                "sentiment_analysis": current_data.sentiment_analysis,
                "prominent_analysis": current_data.prominent_analysis,
            }
        return None

    async def extract_content_site(self, url: str) -> ResponseContent:
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
