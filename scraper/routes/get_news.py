import asyncio
import uuid
from datetime import datetime
import aiohttp
import logging

from blacksheep import HTTPException, json
from scraper.configs.models import Status
from scraper.configs.openapidocs import docs
from scraper.routes.routers import base
from scraper.services.news_service import NewsService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for job tracking (use Redis/database in production)
active_jobs = {}

class WebhookNotifier:
    @staticmethod
    async def send_completion_notification(webhook_url: str, job_id: str, result: dict, error: str = ''):
        """Send webhook notification when scraping is complete"""
        try:
            payload = {
                "job_id": job_id,
                "status": "completed" if not error else "failed",
                "completed_at": datetime.utcnow().isoformat(),
                "result": result if not error else None,
                "error": error,
                "message": "Scraping completed successfully" if not error else f"Scraping failed: {error}"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'NewsScraper-Webhook/1.0'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        logger.info(f"✅ Webhook notification sent successfully for job {job_id}")
                    else:
                        logger.error(f"❌ Webhook failed with status {response.status} for job {job_id}")
                        
        except Exception as e:
            logger.error(f"❌ Failed to send webhook notification for job {job_id}: {str(e)}")

async def background_scraper_task(job_id: str, keyword: str, use_rca: bool, webhook_url: str):
    """Background task that performs the actual scraping"""
    try:
        logger.info(f"🚀 Starting scraping job {job_id} for keyword: {keyword}")
        
        # Update job status to running
        active_jobs[job_id]["status"] = "running"
        active_jobs[job_id]["started_at"] = datetime.utcnow().isoformat()
        
        # Perform the actual scraping
        news_service = NewsService()
        result = await news_service.get_news_by_keyword(keyword.strip(), use_rca)
        
        if result.status == Status.ERROR:
            # Handle scraping error
            active_jobs[job_id]["status"] = "failed"
            active_jobs[job_id]["error"] = result.message
            active_jobs[job_id]["completed_at"] = datetime.utcnow().isoformat()
            
            # Send webhook notification about failure
            await WebhookNotifier.send_completion_notification(
                webhook_url, job_id, {}, error=result.message
            )
        else:
            # Handle successful scraping
            active_jobs[job_id]["status"] = "completed"
            active_jobs[job_id]["result"] = {"message": result.message, "status": result.status.value}
            active_jobs[job_id]["completed_at"] = datetime.utcnow().isoformat()
            
            # Send webhook notification about success
            await WebhookNotifier.send_completion_notification(
                webhook_url, job_id, active_jobs[job_id]["result"]
            )
            
        logger.info(f"✅ Scraping job {job_id} completed with status: {active_jobs[job_id]['status']}")
        
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"❌ Unexpected error in scraping job {job_id}: {str(e)}")
        active_jobs[job_id]["status"] = "failed"
        active_jobs[job_id]["error"] = str(e)
        active_jobs[job_id]["completed_at"] = datetime.utcnow().isoformat()
        
        # Send webhook notification about failure
        await WebhookNotifier.send_completion_notification(
            webhook_url, job_id, {}, error=str(e)
        )

@docs(
    responses={
        202: "Scraping job started successfully - will notify via webhook when complete",
        400: "Bad request - invalid parameters",
        500: "Internal Server Error",
    },
    description="This endpoint will start an async news scraping job and notify via webhook when complete",
    tags=["News"],
)
@base.post("/get-news/")
async def get_news_async(keyword: str, webhook_url: str, use_rca: bool = False):
    """
    Start an async news scraping job that will notify via webhook when complete
    
    @param keyword: The keywords to search
    @param webhook_url: URL to send completion notification to
    @param use_rca: Use Root Cause Analysis
    """
    try:
        # Validate input
        if not keyword or len(keyword.strip()) == 0:
            raise HTTPException(status=400, message="Keyword cannot be empty")
            
        if not webhook_url or not webhook_url.startswith(('http://', 'https://')):
            raise HTTPException(status=400, message="Valid webhook URL is required")

        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Store job info
        active_jobs[job_id] = {
            "job_id": job_id,
            "keyword": keyword.strip(),
            "use_rca": use_rca,
            "webhook_url": webhook_url,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None
        }
        
        # Start background task
        asyncio.create_task(background_scraper_task(job_id, keyword.strip(), use_rca, webhook_url))
        
        return json({
            "message": "Scraping job started successfully. You will receive a webhook notification when complete.",
            "job_id": job_id,
            "status": "queued",
            "webhook_url": webhook_url
        }, status=202)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Unexpected error: {str(e)}")

@docs(
    responses={
        200: "Job status retrieved successfully",
        404: "Job not found",
    },
    description="Check the status of a scraping job",
    tags=["News"],
)
@base.get("/job-status/{job_id}")
async def get_job_status(job_id: str):
    """
    Get the status of a scraping job
    
    @param job_id: The job ID to check
    """
    if job_id not in active_jobs:
        raise HTTPException(status=404, message="Job not found")
    
    job_info = active_jobs[job_id].copy()
    return json(job_info, status=200)

@docs(
    responses={
        200: "Active jobs retrieved successfully",
    },
    description="Get list of all active/recent jobs",
    tags=["News"],
)
@base.get("/jobs/")
async def get_all_jobs():
    """Get list of all jobs"""
    return json({
        "jobs": list(active_jobs.values()),
        "total": len(active_jobs)
    }, status=200)

# Keep the original synchronous endpoint for backwards compatibility
@docs(
    responses={
        200: "News fetched successfully",
        400: "Bad request - invalid parameters", 
        500: "Internal Server Error",
    },
    description="This endpoint will fetch news from Google News based on the keywords provided (synchronous)",
    tags=["News"],
)
@base.get("/get-news/")
async def get_news(keyword: str, use_rca: bool = False):
    """
    Getting news list from Google News (synchronous - may take a while)

    @param keyword: The keywords to search
    @param use_rca: Use Root Cause Analysis
    """
    try:
        # Validate input
        if not keyword or len(keyword.strip()) == 0:
            raise HTTPException(status=400, message="Keyword cannot be empty")

        # Get service and fetch news
        news_service = NewsService()
        result = await news_service.get_news_by_keyword(keyword.strip(), use_rca)

        if result.status == Status.ERROR:
            raise HTTPException(status=500, message=result.message)

        return json({"message": result.message, "status": result.status.value}, status=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status=500, message=f"Unexpected error: {str(e)}")