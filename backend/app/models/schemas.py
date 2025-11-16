"""Pydantic models for request/response schemas."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RecordBase(BaseModel):
    """Base record model."""

    id: Optional[str] = None
    fields: Dict[str, str] = Field(..., description="Record fields as key-value pairs")


class RecordPair(BaseModel):
    """Model for a pair of records to compare."""

    record_a: RecordBase
    record_b: RecordBase


class MatchPrediction(BaseModel):
    """Model for match prediction result."""

    is_match: bool
    match_probability: float = Field(..., ge=0.0, le=1.0)
    confidence: str = Field(..., description="High, Medium, or Low")
    similarity_score: float = Field(..., ge=0.0, le=1.0)


class FeatureContribution(BaseModel):
    """Model for individual feature contribution."""

    field_name: str
    contribution: float
    value_a: str
    value_b: str


class TokenContribution(BaseModel):
    """Model for token-level contribution."""

    token: str
    contribution: float
    position: int


class Explanation(BaseModel):
    """Model for match explanation."""

    method: str = Field(..., description="Explanation method (SHAP)")
    feature_contributions: List[FeatureContribution]
    token_contributions: Optional[List[TokenContribution]] = None
    top_positive_features: List[str]
    top_negative_features: List[str]


class MatchResult(BaseModel):
    """Complete match result with prediction and explanation."""

    prediction: MatchPrediction
    explanation: Optional[Explanation] = None
    record_pair: RecordPair


class BatchMatchRequest(BaseModel):
    """Request model for batch matching."""

    dataset_a: List[RecordBase]
    dataset_b: List[RecordBase]
    threshold: Optional[float] = None
    include_explanations: bool = False


class BatchMatchResult(BaseModel):
    """Result model for batch matching."""

    total_comparisons: int
    matches_found: int
    match_results: List[MatchResult]
    processing_time: float


class DatasetInfo(BaseModel):
    """Information about a dataset."""

    name: str
    description: str
    num_records: int
    fields: List[str]
    sample_records: Optional[List[RecordBase]] = None


class HealthCheck(BaseModel):
    """Health check response."""

    status: str
    version: str
    model_loaded: bool
    device: str


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    status_code: int
