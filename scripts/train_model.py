#!/usr/bin/env python3
"""Train the entity matching model."""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.ml.training import train_model, evaluate_model
from app.ml.model import EntityMatchingModel
from app.core.config import settings


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(
        description="Train entity matching model"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to training dataset CSV or dataset name (uci, dblp_acm, etc.)",
    )
    parser.add_argument(
        "--test-dataset",
        type=str,
        help="Path to test dataset CSV for evaluation",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default=settings.MODEL_NAME,
        help=f"Pre-trained model name (default: {settings.MODEL_NAME})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path for fine-tuned model",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs (default: 10)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size (default: 32)",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-5,
        help="Learning rate (default: 2e-5)",
    )

    args = parser.parse_args()

    # Resolve dataset path
    if not args.dataset.endswith(".csv"):
        # Assume it's a dataset name
        data_dir = Path(__file__).parent.parent / "data" / "raw"
        dataset_files = {
            "uci": "uci_record_linkage.csv",
            "dblp_acm": "dblp_acm.csv",
            "dblp_scholar_dirty": "dblp_scholar_dirty.csv",
            "walmart_amazon": "walmart_amazon.csv",
        }
        dataset_key = args.dataset.lower().replace("-", "_")
        if dataset_key in dataset_files:
            train_data_path = str(data_dir / dataset_files[dataset_key])
        else:
            print(f"Unknown dataset: {args.dataset}")
            print(f"Available datasets: {', '.join(dataset_files.keys())}")
            sys.exit(1)
    else:
        train_data_path = args.dataset

    print("Training Configuration:")
    print(f"  Dataset: {train_data_path}")
    print(f"  Model: {args.model_name}")
    print(f"  Epochs: {args.epochs}")
    print(f"  Batch size: {args.batch_size}")
    print(f"  Learning rate: {args.learning_rate}")
    print()

    # Train the model
    try:
        train_model(
            train_data_path=train_data_path,
            model_name=args.model_name,
            output_path=args.output,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
        )

        # Evaluate if test dataset provided
        if args.test_dataset:
            print("\nEvaluating on test set...")
            model = EntityMatchingModel(model_name=args.model_name)
            output_path = args.output or f"{settings.MODEL_PATH}/fine_tuned"
            model.load_fine_tuned(output_path)

            metrics = evaluate_model(
                model=model,
                test_data_path=args.test_dataset,
                threshold=settings.SIMILARITY_THRESHOLD,
            )

    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    print("\nTraining complete!")


if __name__ == "__main__":
    main()
