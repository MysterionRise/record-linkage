"""BERT-based entity matching model."""

import torch
from sentence_transformers import SentenceTransformer
from typing import Tuple, List
import os

from app.core.config import settings


class EntityMatchingModel:
    """BERT-based entity matching model using sentence transformers."""

    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize the entity matching model.

        Args:
            model_name: Name of the pre-trained model
            device: Device to run on (cpu/cuda)
        """
        self.model_name = model_name or settings.MODEL_NAME
        self.device = device or self._get_device()
        self.model = None
        self.is_loaded = False

    def _get_device(self) -> str:
        """Get the appropriate device (CPU or CUDA)."""
        if settings.DEVICE == "cuda" and torch.cuda.is_available():
            return "cuda"
        return "cpu"

    def load_model(self):
        """Load the pre-trained sentence transformer model."""
        print(f"Loading model: {self.model_name}")
        print(f"Device: {self.device}")

        try:
            self.model = SentenceTransformer(self.model_name, device=self.device)
            self.is_loaded = True
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def encode(self, texts: List[str], batch_size: int = None) -> torch.Tensor:
        """
        Encode texts into embeddings.

        Args:
            texts: List of texts to encode
            batch_size: Batch size for encoding

        Returns:
            torch.Tensor: Embeddings
        """
        if not self.is_loaded:
            self.load_model()

        batch_size = batch_size or settings.BATCH_SIZE

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_tensor=True,
            show_progress_bar=False,
        )

        return embeddings

    def compute_similarity(
        self, text_a: str, text_b: str
    ) -> Tuple[float, torch.Tensor, torch.Tensor]:
        """
        Compute similarity between two texts.

        Args:
            text_a: First text
            text_b: Second text

        Returns:
            Tuple of (similarity_score, embedding_a, embedding_b)
        """
        if not self.is_loaded:
            self.load_model()

        # Encode both texts
        embeddings = self.encode([text_a, text_b])
        embedding_a = embeddings[0]
        embedding_b = embeddings[1]

        # Compute cosine similarity
        similarity = torch.cosine_similarity(embedding_a.unsqueeze(0), embedding_b.unsqueeze(0))

        return similarity.item(), embedding_a, embedding_b

    def predict_batch(self, text_pairs: List[Tuple[str, str]]) -> List[float]:
        """
        Predict similarity for a batch of text pairs.

        Args:
            text_pairs: List of (text_a, text_b) tuples

        Returns:
            List of similarity scores
        """
        if not self.is_loaded:
            self.load_model()

        # Separate texts
        texts_a = [pair[0] for pair in text_pairs]
        texts_b = [pair[1] for pair in text_pairs]

        # Encode all texts
        embeddings_a = self.encode(texts_a)
        embeddings_b = self.encode(texts_b)

        # Compute similarities
        similarities = torch.cosine_similarity(embeddings_a, embeddings_b)

        return similarities.tolist()

    def save_model(self, path: str = None):
        """
        Save the fine-tuned model.

        Args:
            path: Path to save the model
        """
        if not self.is_loaded:
            raise ValueError("No model loaded to save")

        save_path = path or os.path.join(settings.MODEL_PATH, "fine_tuned")
        os.makedirs(save_path, exist_ok=True)

        self.model.save(save_path)
        print(f"Model saved to: {save_path}")

    def load_fine_tuned(self, path: str):
        """
        Load a fine-tuned model.

        Args:
            path: Path to the fine-tuned model
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found at: {path}")

        print(f"Loading fine-tuned model from: {path}")
        self.model = SentenceTransformer(path, device=self.device)
        self.is_loaded = True
        print("Fine-tuned model loaded successfully!")


# Global model instance
_model_instance = None


def get_model() -> EntityMatchingModel:
    """
    Get or create the global model instance.

    Returns:
        EntityMatchingModel: The global model instance
    """
    global _model_instance

    if _model_instance is None:
        _model_instance = EntityMatchingModel()

    return _model_instance
