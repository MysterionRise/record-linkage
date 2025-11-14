"""Dataset management endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File
import os
import json

from app.core.config import settings
from app.models.schemas import DatasetInfo, RecordBase
from app.utils.data_loader import load_dataset, list_available_datasets

router = APIRouter()


@router.get("/", response_model=List[DatasetInfo])
async def list_datasets():
    """
    List all available datasets.

    Returns:
        List[DatasetInfo]: List of available datasets with metadata
    """
    try:
        datasets = list_available_datasets()
        return datasets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{dataset_name}", response_model=DatasetInfo)
async def get_dataset_info(dataset_name: str, include_samples: bool = True):
    """
    Get information about a specific dataset.

    Args:
        dataset_name: Name of the dataset
        include_samples: Whether to include sample records

    Returns:
        DatasetInfo: Dataset information and optional samples
    """
    try:
        dataset_info = load_dataset(dataset_name, include_samples=include_samples)
        return dataset_info
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a custom dataset.

    Args:
        file: CSV file containing records

    Returns:
        dict: Upload status and dataset name
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    try:
        # Save uploaded file
        file_path = os.path.join(settings.RAW_DATA_DIR, file.filename)
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        return {
            "status": "success",
            "filename": file.filename,
            "message": "Dataset uploaded successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
