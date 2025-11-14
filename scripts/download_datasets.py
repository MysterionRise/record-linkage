#!/usr/bin/env python3
"""Download datasets for record linkage experiments."""

import os
import urllib.request
import zipfile
import pandas as pd
from pathlib import Path


def download_file(url: str, dest_path: str):
    """Download a file from URL."""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"Saved to {dest_path}")


def download_uci_dataset(data_dir: str):
    """
    Download UCI Record Linkage Comparison Patterns dataset.

    URL: https://archive.ics.uci.edu/ml/datasets/record+linkage+comparison+patterns
    """
    print("\n=== Downloading UCI Record Linkage Dataset ===")

    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00210/donation.zip"
    zip_path = os.path.join(data_dir, "uci_donation.zip")

    try:
        download_file(url, zip_path)

        # Extract zip
        print("Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)

        print("UCI dataset downloaded successfully!")

        # Clean up zip file
        os.remove(zip_path)

    except Exception as e:
        print(f"Error downloading UCI dataset: {e}")
        print("Please download manually from:")
        print("https://archive.ics.uci.edu/ml/datasets/record+linkage+comparison+patterns")


def create_sample_datasets(data_dir: str):
    """Create sample datasets for demo purposes."""
    print("\n=== Creating Sample Datasets ===")

    # Sample DBLP-ACM dataset
    dblp_acm_data = {
        'title_a': [
            'Deep Learning for Entity Matching',
            'Record Linkage and Machine Learning',
            'BERT for Natural Language Processing',
        ],
        'author_a': [
            'John Smith, Jane Doe',
            'Alice Johnson',
            'Bob Wilson, Carol White',
        ],
        'venue_a': [
            'SIGMOD',
            'KDD',
            'ACL',
        ],
        'year_a': [2018, 2020, 2019],
        'title_b': [
            'Deep Learning for Entity Matching: A Design Space',
            'Machine Learning for Record Linkage',
            'BERT: Pre-training for NLP',
        ],
        'author_b': [
            'J. Smith, J. Doe',
            'A. Johnson',
            'Robert Wilson, C. White',
        ],
        'venue_b': [
            'SIGMOD Conference',
            'KDD Conference',
            'ACL',
        ],
        'year_b': [2018, 2020, 2019],
        'label': [1, 1, 1],  # All matches
    }

    df_dblp_acm = pd.DataFrame(dblp_acm_data)
    output_path = os.path.join(data_dir, 'raw', 'dblp_acm.csv')
    df_dblp_acm.to_csv(output_path, index=False)
    print(f"Created sample DBLP-ACM dataset: {output_path}")

    # Sample Walmart-Amazon product dataset
    walmart_amazon_data = {
        'title_a': [
            'Apple iPhone 13 Pro Max 256GB',
            'Sony WH-1000XM4 Wireless Headphones',
            'Dell XPS 15 Laptop',
        ],
        'brand_a': ['Apple', 'Sony', 'Dell'],
        'price_a': [1099.00, 349.99, 1499.99],
        'category_a': ['Electronics > Phones', 'Electronics > Audio', 'Electronics > Computers'],
        'title_b': [
            'iPhone 13 Pro Max - 256GB - Apple',
            'Sony WH1000XM4 Noise Cancelling Headphones',
            'Dell XPS 15 9510 15.6" Laptop',
        ],
        'brand_b': ['Apple', 'Sony', 'Dell'],
        'price_b': [1099.00, 348.00, 1499.00],
        'category_b': ['Cell Phones', 'Headphones', 'Laptops'],
        'label': [1, 1, 1],
    }

    df_walmart_amazon = pd.DataFrame(walmart_amazon_data)
    output_path = os.path.join(data_dir, 'raw', 'walmart_amazon.csv')
    df_walmart_amazon.to_csv(output_path, index=False)
    print(f"Created sample Walmart-Amazon dataset: {output_path}")

    # Sample dirty dataset (DBLP-Scholar with issues)
    dblp_scholar_dirty_data = {
        'title_a': [
            'Deep Learning for Entity Matching',
            'Record Linkage and Machine Learning',
            'BERT for Natural Language Processing',
        ],
        'author_a': [
            'John Smith, Jane Doe',
            'Alice Johnson',
            'Bob Wilson',
        ],
        'venue_a': ['SIGMOD', 'KDD', 'ACL'],
        'year_a': [2018, 2020, 2019],
        'title_b': [
            'Deep Learing for Entty Matching',  # Typos
            'ML for Record Linkge',  # Abbreviation + typo
            'BERT Pre-training',  # Incomplete
        ],
        'author_b': [
            'J Smith, J. Doe',  # Missing period
            'A Johnson',  # Missing period
            'Robert Wilson',  # Different first name
        ],
        'venue_b': ['SIGMOD Conf', 'KDD', 'ACL 2019'],
        'year_b': ['2018', '2020', ''],  # Missing year
        'label': [1, 1, 0],  # Last one is actually different
    }

    df_dirty = pd.DataFrame(dblp_scholar_dirty_data)
    output_path = os.path.join(data_dir, 'raw', 'dblp_scholar_dirty.csv')
    df_dirty.to_csv(output_path, index=False)
    print(f"Created sample DBLP-Scholar (Dirty) dataset: {output_path}")


def main():
    """Main function to download all datasets."""
    # Get project root directory
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent
    data_dir = project_root / "data"
    raw_dir = data_dir / "raw"
    processed_dir = data_dir / "processed"

    # Create directories if they don't exist
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    print("Record Linkage Dataset Downloader")
    print("=" * 50)
    print(f"Data directory: {data_dir}")

    # Download UCI dataset (optional, may require manual download)
    response = input("\nDownload UCI dataset? (y/n): ")
    if response.lower() == 'y':
        download_uci_dataset(str(raw_dir))

    # Create sample datasets
    create_sample_datasets(str(data_dir))

    print("\n" + "=" * 50)
    print("Dataset setup complete!")
    print(f"Raw data saved to: {raw_dir}")
    print(f"Processed data will be saved to: {processed_dir}")
    print("\nNote: Some datasets may need to be downloaded manually.")
    print("See IMPLEMENTATION_PLAN.md for dataset sources.")


if __name__ == "__main__":
    main()
