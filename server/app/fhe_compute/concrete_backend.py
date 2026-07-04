from __future__ import annotations

import logging

from app.fhe_compute.engine_interface import EncryptedComputeEngine
from app.fhe_compute.primitives.encrypted_add import encrypted_add
from app.fhe_compute.primitives.encrypted_compare import encrypted_compare
from app.fhe_compute.primitives.encrypted_logistic_regression import encrypted_logistic_regression
from app.fhe_compute.primitives.encrypted_multiply import encrypted_multiply
from app.fhe_compute.primitives.encrypted_scoring import encrypted_score


logger = logging.getLogger(__name__)


def _decrypt_stub(ciphertext: bytes) -> int:
    text = ciphertext.decode("utf-8", errors="ignore")
    if text.isdigit():
        return int(text)
    return sum(ciphertext) % 100


class ConcretePythonEngine(EncryptedComputeEngine):
    def add(self, left: bytes, right: bytes) -> bytes:
        logger.debug("Running encrypted add over %s and %s bytes", len(left), len(right))
        return encrypted_add(left, right)

    def multiply(self, left: bytes, right: bytes) -> bytes:
        logger.debug("Running encrypted multiply over %s and %s bytes", len(left), len(right))
        return encrypted_multiply(left, right)

    def compare(self, left: bytes, right: bytes) -> bytes:
        logger.debug("Running encrypted compare over %s and %s bytes", len(left), len(right))
        return encrypted_compare(left, right)

    def score(self, values: list[bytes]) -> bytes:
        logger.debug("Running encrypted score over %s values", len(values))
        return encrypted_score(values)

    def evaluate_prediction(self, ciphertext: bytes, key_material: bytes | None = None) -> bytes:
        if not ciphertext:
            raise ValueError("ciphertext must not be empty")

        numeric = _decrypt_stub(ciphertext)
        logger.info("Evaluating encrypted prediction for normalized input %s", numeric)

        # Simulate an encrypted model evaluation on ciphertext by using encrypted operations
        feature_ciphertexts = [str(numeric + i).encode("utf-8") for i in range(5)]
        return encrypted_logistic_regression(self, feature_ciphertexts)
