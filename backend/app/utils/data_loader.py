"""Dataset loading utilities."""

import os
import pandas as pd
from typing import List

from app.core.config import settings
from app.models.schemas import DatasetInfo, RecordBase


def list_available_datasets() -> List[DatasetInfo]:
    """
    List all available datasets in the data directory.

    Returns:
        List[DatasetInfo]: List of available datasets
    """
    datasets = []

    # Pre-defined datasets
    dataset_configs = {
        "uci": {
            "name": "UCI Record Linkage",
            "description": "UCI Record Linkage Comparison Patterns (~574K pairs)",
            "file": "uci_record_linkage.csv",
        },
        "dblp_acm": {
            "name": "DBLP-ACM",
            "description": "Academic publications from DBLP and ACM (clean data)",
            "file": "dblp_acm.csv",
        },
        "dblp_scholar_dirty": {
            "name": "DBLP-Scholar (Dirty)",
            "description": "Academic publications with data quality issues",
            "file": "dblp_scholar_dirty.csv",
        },
        "walmart_amazon": {
            "name": "Walmart-Amazon",
            "description": "E-commerce product matching (~10K pairs)",
            "file": "walmart_amazon.csv",
        },
    }

    for dataset_id, config in dataset_configs.items():
        file_path = os.path.join(settings.RAW_DATA_DIR, config["file"])

        # Check if file exists and get record count
        num_records = 0
        fields = []

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path, nrows=1)
                fields = df.columns.tolist()
                df_full = pd.read_csv(file_path)
                num_records = len(df_full)
            except Exception:
                pass

        datasets.append(
            DatasetInfo(
                name=config["name"],
                description=config["description"],
                num_records=num_records,
                fields=fields,
            )
        )

    return datasets


def load_dataset(
    dataset_name: str, include_samples: bool = True, num_samples: int = 5
) -> DatasetInfo:
    """
    Load a specific dataset and return its information.

    Args:
        dataset_name: Name of the dataset to load
        include_samples: Whether to include sample records
        num_samples: Number of sample records to include

    Returns:
        DatasetInfo: Dataset information with optional samples

    Raises:
        FileNotFoundError: If dataset file doesn't exist
    """
    # Map dataset names to files
    dataset_files = {
        "uci": "uci_record_linkage.csv",
        "dblp_acm": "dblp_acm.csv",
        "dblp_scholar_dirty": "dblp_scholar_dirty.csv",
        "walmart_amazon": "walmart_amazon.csv",
    }

    # Normalize dataset name
    dataset_key = dataset_name.lower().replace(" ", "_").replace("-", "_")

    if dataset_key not in dataset_files:
        raise FileNotFoundError(f"Dataset '{dataset_name}' not found")

    file_path = os.path.join(settings.RAW_DATA_DIR, dataset_files[dataset_key])

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}. "
            "Run scripts/download_datasets.py to download datasets."
        )

    # Load dataset
    df = pd.read_csv(file_path)
    fields = df.columns.tolist()

    # Get sample records if requested
    sample_records = None
    if include_samples:
        sample_df = df.head(num_samples)
        sample_records = [
            RecordBase(
                id=str(idx),
                fields={col: str(row[col]) for col in df.columns},
            )
            for idx, row in sample_df.iterrows()
        ]

    # Get dataset description
    descriptions = {
        "uci": "UCI Record Linkage Comparison Patterns (~574K pairs)",
        "dblp_acm": "Academic publications from DBLP and ACM (clean data)",
        "dblp_scholar_dirty": "Academic publications with data quality issues",
        "walmart_amazon": "E-commerce product matching (~10K pairs)",
    }

    return DatasetInfo(
        name=dataset_name,
        description=descriptions.get(dataset_key, "Unknown dataset"),
        num_records=len(df),
        fields=fields,
        sample_records=sample_records,
    )


def load_records_from_csv(file_path: str) -> List[RecordBase]:
    """
    Load records from a CSV file.

    Args:
        file_path: Path to the CSV file

    Returns:
        List[RecordBase]: List of records
    """
    df = pd.read_csv(file_path)
    records = [
        RecordBase(
            id=str(idx),
            fields={col: str(row[col]) for col in df.columns},
        )
        for idx, row in df.iterrows()
    ]
    return records
