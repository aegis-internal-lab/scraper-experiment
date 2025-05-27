from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class NewsRequestSchema(BaseModel):
    """Schema for news request"""

    keyword: str = Field(..., min_length=1, max_length=100, description="Search keyword")
    use_rca: bool = Field(default=False, description="Whether to perform root cause analysis")


class AnalysisRequestSchema(BaseModel):
    """Schema for analysis request"""

    url: HttpUrl = Field(..., description="URL to analyze")


class NewsResponseSchema(BaseModel):
    """Schema for news response"""

    message: str
    status: str


class AnalysisResponseSchema(BaseModel):
    """Schema for analysis response"""

    url: str
    masked_url: Optional[str] = None
    rc_analysis: Optional[str] = None
    sentiment_analysis: Optional[str] = None
    prominent_analysis: Optional[str] = None


class SiteSchema(BaseModel):
    """Schema for site data"""

    id: int
    title: Optional[str]
    published_date: str
    keyword: str
    content: Optional[str]
    masked_url: str
    url: str
    is_extracted: bool
    has_rc_analysis: bool
    rc_analysis: Optional[str]
    has_sentiment_analysis: bool
    sentiment_analysis: Optional[str]
    has_prominent_analysis: bool
    prominent_analysis: Optional[str]
    created_at: str
    updated_at: str


class ErrorResponseSchema(BaseModel):
    """Schema for error responses"""

    error: str
    message: str
    status_code: int
