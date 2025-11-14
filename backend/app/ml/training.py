"""Training pipeline for entity matching model."""

import torch
from torch.utils.data import Dataset, DataLoader
from sentence_transformers import InputExample, losses
from typing import List, Tuple
import pandas as pd

from app.ml.model import EntityMatchingModel
from app.core.config import settings


class RecordPairDataset(Dataset):
    """Dataset for record pairs."""

    def __init__(self, pairs: List[Tuple[str, str, int]]):
        """
        Initialize dataset.

        Args:
            pairs: List of (text_a, text_b, label) tuples
        """
        self.pairs = pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        return self.pairs[idx]


def load_training_data(
    dataset_path: str,
) -> List[InputExample]:
    """
    Load training data from a CSV file.

    Expected CSV format:
    - label: 0/1 indicating match/no-match
    - Additional columns representing record fields

    Args:
        dataset_path: Path to training data CSV

    Returns:
        List of InputExample for training
    """
    df = pd.read_csv(dataset_path)

    if "label" not in df.columns:
        raise ValueError("Training data must have a 'label' column")

    examples = []

    # Group columns into record A and record B
    # Assume columns are named like: field1_a, field1_b, field2_a, field2_b, etc.
    field_names = set()
    for col in df.columns:
        if col.endswith("_a"):
            field_name = col[:-2]
            field_names.add(field_name)

    for _, row in df.iterrows():
        # Construct record A and B
        parts_a = []
        parts_b = []

        for field in sorted(field_names):
            col_a = f"{field}_a"
            col_b = f"{field}_b"

            if col_a in df.columns and col_b in df.columns:
                val_a = str(row[col_a])
                val_b = str(row[col_b])

                if val_a and val_a not in ["nan", "None"]:
                    parts_a.append(f"{field}: {val_a}")
                if val_b and val_b not in ["nan", "None"]:
                    parts_b.append(f"{field}: {val_b}")

        text_a = " | ".join(parts_a)
        text_b = " | ".join(parts_b)
        label = float(row["label"])

        examples.append(InputExample(texts=[text_a, text_b], label=label))

    return examples


def train_model(
    train_data_path: str,
    model_name: str = None,
    output_path: str = None,
    epochs: int = 10,
    batch_size: int = 32,
    learning_rate: float = 2e-5,
):
    """
    Train the entity matching model.

    Args:
        train_data_path: Path to training data CSV
        model_name: Name of pre-trained model to fine-tune
        output_path: Path to save fine-tuned model
        epochs: Number of training epochs
        batch_size: Batch size
        learning_rate: Learning rate
    """
    print("Loading training data...")
    train_examples = load_training_data(train_data_path)
    print(f"Loaded {len(train_examples)} training examples")

    print("Initializing model...")
    model = EntityMatchingModel(model_name=model_name)
    model.load_model()

    # Create data loader
    train_dataloader = DataLoader(
        train_examples, shuffle=True, batch_size=batch_size
    )

    # Define loss function
    train_loss = losses.CosineSimilarityLoss(model.model)

    # Train the model
    print("Starting training...")
    model.model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=int(len(train_dataloader) * 0.1),
        optimizer_params={"lr": learning_rate},
        show_progress_bar=True,
    )

    # Save the fine-tuned model
    output_path = output_path or f"{settings.MODEL_PATH}/fine_tuned"
    model.save_model(output_path)
    print(f"Model saved to {output_path}")


def evaluate_model(
    model: EntityMatchingModel,
    test_data_path: str,
    threshold: float = 0.75,
) -> dict:
    """
    Evaluate model performance on test data.

    Args:
        model: Trained model
        test_data_path: Path to test data CSV
        threshold: Classification threshold

    Returns:
        dict: Evaluation metrics
    """
    print("Loading test data...")
    df = pd.read_csv(test_data_path)

    if "label" not in df.columns:
        raise ValueError("Test data must have a 'label' column")

    # Get field names
    field_names = set()
    for col in df.columns:
        if col.endswith("_a"):
            field_name = col[:-2]
            field_names.add(field_name)

    # Prepare test pairs
    test_pairs = []
    true_labels = []

    for _, row in df.iterrows():
        parts_a = []
        parts_b = []

        for field in sorted(field_names):
            col_a = f"{field}_a"
            col_b = f"{field}_b"

            if col_a in df.columns and col_b in df.columns:
                val_a = str(row[col_a])
                val_b = str(row[col_b])

                if val_a and val_a not in ["nan", "None"]:
                    parts_a.append(f"{field}: {val_a}")
                if val_b and val_b not in ["nan", "None"]:
                    parts_b.append(f"{field}: {val_b}")

        text_a = " | ".join(parts_a)
        text_b = " | ".join(parts_b)

        test_pairs.append((text_a, text_b))
        true_labels.append(int(row["label"]))

    # Get predictions
    print("Making predictions...")
    similarities = model.predict_batch(test_pairs)
    predictions = [1 if sim >= threshold else 0 for sim in similarities]

    # Calculate metrics
    true_positives = sum(
        p == 1 and t == 1 for p, t in zip(predictions, true_labels)
    )
    false_positives = sum(
        p == 1 and t == 0 for p, t in zip(predictions, true_labels)
    )
    false_negatives = sum(
        p == 0 and t == 1 for p, t in zip(predictions, true_labels)
    )
    true_negatives = sum(
        p == 0 and t == 0 for p, t in zip(predictions, true_labels)
    )

    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0
    )
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )
    accuracy = (true_positives + true_negatives) / len(true_labels)

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "true_negatives": true_negatives,
    }

    print("\nEvaluation Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    return metrics
