"""Entity matching endpoints."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    RecordPair,
    MatchResult,
    BatchMatchRequest,
    BatchMatchResult,
)
from app.ml.inference import predict_match, batch_predict

router = APIRouter()


@router.post("/predict", response_model=MatchResult)
async def predict_record_match(
    record_pair: RecordPair,
    include_explanation: bool = True,
):
    """
    Predict if two records match.

    Args:
        record_pair: Pair of records to compare
        include_explanation: Whether to include SHAP explainability

    Returns:
        MatchResult: Match prediction with optional SHAP explanation
    """
    try:
        result = await predict_match(
            record_pair,
            include_explanation=include_explanation,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/batch", response_model=BatchMatchResult)
async def batch_match_records(request: BatchMatchRequest):
    """
    Perform batch matching between two datasets.

    Args:
        request: Batch matching request with two datasets

    Returns:
        BatchMatchResult: Results of all comparisons
    """
    try:
        result = await batch_predict(
            dataset_a=request.dataset_a,
            dataset_b=request.dataset_b,
            threshold=request.threshold,
            include_explanations=request.include_explanations,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch matching failed: {str(e)}")


@router.get("/threshold/optimize")
async def optimize_threshold(dataset_name: str):
    """
    Find optimal threshold for a dataset using ROC curve analysis.

    Args:
        dataset_name: Name of the labeled dataset

    Returns:
        dict: Optimal threshold and metrics
    """
    # TODO: Implement threshold optimization
    raise HTTPException(status_code=501, detail="Threshold optimization not yet implemented")
