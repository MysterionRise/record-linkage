"""Explainability utilities using SHAP and LIME."""

import shap
import numpy as np
from typing import List, Tuple, Dict
from lime.lime_text import LimeTextExplainer

from app.models.schemas import (
    RecordPair,
    Explanation,
    FeatureContribution,
    TokenContribution,
)
from app.ml.preprocessing import serialize_record_pair, extract_field_pairs
from app.ml.model import EntityMatchingModel


class RecordLinkageExplainer:
    """Explainer for record linkage predictions."""

    def __init__(self, model: EntityMatchingModel):
        """
        Initialize explainer.

        Args:
            model: The entity matching model to explain
        """
        self.model = model
        self.lime_explainer = LimeTextExplainer(class_names=["No Match", "Match"])

    def explain_with_shap(self, record_pair: RecordPair, num_samples: int = 100) -> Explanation:
        """
        Generate SHAP-based explanation for a prediction.

        Args:
            record_pair: Pair of records to explain
            num_samples: Number of samples for SHAP

        Returns:
            Explanation: SHAP-based explanation
        """
        # Serialize the record pair
        text = serialize_record_pair(record_pair, add_sep=True)

        # Get field pairs for field-level attribution
        field_pairs = extract_field_pairs(record_pair)

        # TODO: Implement actual SHAP explanation
        # For now, use field-based heuristics as placeholder

        feature_contributions = []
        top_positive = []
        top_negative = []

        for field_name, value_a, value_b in field_pairs:
            # Simple similarity heuristic
            value_a_norm = value_a.lower().strip()
            value_b_norm = value_b.lower().strip()

            if value_a_norm == value_b_norm:
                contribution = 0.8
                top_positive.append(field_name)
            elif value_a_norm in value_b_norm or value_b_norm in value_a_norm:
                contribution = 0.4
                if contribution > 0.3:
                    top_positive.append(field_name)
            else:
                # Use actual model to compute field contribution
                field_text = f"{value_a} [SEP] {value_b}"
                try:
                    embeddings = self.model.encode([field_text])
                    # Normalize to contribution range
                    contribution = float(np.mean(embeddings.cpu().numpy())) * 0.1
                except Exception:
                    contribution = -0.2

                if contribution < 0:
                    top_negative.append(field_name)

            feature_contributions.append(
                FeatureContribution(
                    field_name=field_name,
                    contribution=contribution,
                    value_a=value_a,
                    value_b=value_b,
                )
            )

        # Sort by absolute contribution
        feature_contributions.sort(key=lambda x: abs(x.contribution), reverse=True)

        return Explanation(
            method="SHAP",
            feature_contributions=feature_contributions,
            top_positive_features=top_positive[:5],
            top_negative_features=top_negative[:5],
        )

    def explain_with_lime(self, record_pair: RecordPair, num_features: int = 10) -> Explanation:
        """
        Generate LIME-based explanation for a prediction.

        Args:
            record_pair: Pair of records to explain
            num_features: Number of features to explain

        Returns:
            Explanation: LIME-based explanation
        """
        # Serialize the record pair
        text = serialize_record_pair(record_pair, add_sep=True)

        # Define prediction function for LIME
        def predict_fn(texts):
            """Prediction function for LIME."""
            # For each perturbed text, compute similarity
            similarities = []
            for t in texts:
                try:
                    # Use model to encode and compute similarity
                    embeddings = self.model.encode([t])
                    # Return probability for both classes
                    sim = float(np.mean(embeddings.cpu().numpy()))
                    # Normalize to [0, 1]
                    sim = (sim + 1) / 2
                    similarities.append([1 - sim, sim])
                except Exception:
                    similarities.append([0.5, 0.5])

            return np.array(similarities)

        try:
            # Generate LIME explanation
            exp = self.lime_explainer.explain_instance(
                text,
                predict_fn,
                num_features=num_features,
                num_samples=100,
            )

            # Extract feature weights
            weights = exp.as_list()

            # Convert to field contributions
            field_pairs = extract_field_pairs(record_pair)
            feature_contributions = []

            for field_name, value_a, value_b in field_pairs:
                # Find relevant weights for this field
                field_contribution = 0.0
                for word, weight in weights:
                    if word.lower() in value_a.lower() or word.lower() in value_b.lower():
                        field_contribution += weight

                feature_contributions.append(
                    FeatureContribution(
                        field_name=field_name,
                        contribution=field_contribution,
                        value_a=value_a,
                        value_b=value_b,
                    )
                )

            # Sort by contribution
            feature_contributions.sort(key=lambda x: abs(x.contribution), reverse=True)

            top_positive = [fc.field_name for fc in feature_contributions if fc.contribution > 0][
                :5
            ]
            top_negative = [fc.field_name for fc in feature_contributions if fc.contribution < 0][
                :5
            ]

            return Explanation(
                method="LIME",
                feature_contributions=feature_contributions,
                top_positive_features=top_positive,
                top_negative_features=top_negative,
            )

        except Exception as e:
            # Fallback to simple explanation
            print(f"LIME explanation failed: {e}")
            return self.explain_with_shap(record_pair)

    def explain(self, record_pair: RecordPair, method: str = "shap") -> Explanation:
        """
        Generate explanation using specified method.

        Args:
            record_pair: Pair of records to explain
            method: Explanation method (shap or lime)

        Returns:
            Explanation: Generated explanation
        """
        method = method.lower()

        if method == "lime":
            return self.explain_with_lime(record_pair)
        else:
            return self.explain_with_shap(record_pair)
