from __future__ import annotations

import logging

from app.fhe_compute.engine_interface import EncryptedComputeEngine
from app.fhe_compute.model_weights import MODEL_COEFFICIENTS, MODEL_BIAS

logger = logging.getLogger(__name__)


def encrypted_logistic_regression(
    engine: EncryptedComputeEngine,
    feature_ciphertexts: list[bytes],
) -> bytes:
    if not isinstance(feature_ciphertexts, list):
        raise TypeError("feature_ciphertexts must be a list of bytes-like values")
    if len(feature_ciphertexts) != len(MODEL_COEFFICIENTS):
        raise ValueError(
            f"expected {len(MODEL_COEFFICIENTS)} feature ciphertexts, got {len(feature_ciphertexts)}"
        )

    for index, feature in enumerate(feature_ciphertexts):
        if not isinstance(feature, (bytes, bytearray)):
            raise TypeError(f"feature_ciphertexts[{index}] must be bytes-like")

    logger.info("Computing encrypted logistic regression score for %s encrypted features", len(feature_ciphertexts))

    weighted_terms = []
    for feature, weight in zip(feature_ciphertexts, MODEL_COEFFICIENTS):
        weight_payload = str(weight).encode("utf-8")
        weighted_terms.append(engine.multiply(feature, weight_payload))

    linear_combination = weighted_terms[0]
    for term in weighted_terms[1:]:
        linear_combination = engine.add(linear_combination, term)

    bias_ciphertext = str(MODEL_BIAS).encode("utf-8")
    linear_with_bias = engine.add(linear_combination, bias_ciphertext)

    # Logistic regression decision boundary: compare the signed linear combination against zero.
    # This produces an encrypted binary classification result without revealing the raw score.
    prediction_ciphertext = engine.compare(linear_with_bias, b"0")
    return prediction_ciphertext
