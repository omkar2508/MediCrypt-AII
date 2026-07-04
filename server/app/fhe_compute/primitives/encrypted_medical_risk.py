from __future__ import annotations

import logging

from app.fhe_compute.engine_interface import EncryptedComputeEngine


logger = logging.getLogger(__name__)


def _ensure_bytes(value: bytes | bytearray, field_name: str) -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError(f"{field_name} must be bytes-like")
    return bytes(value)


def encrypted_medical_risk_score(
    engine: EncryptedComputeEngine,
    age_ciphertext: bytes,
    glucose_ciphertext: bytes,
    blood_pressure_ciphertext: bytes,
    bmi_ciphertext: bytes,
    insulin_ciphertext: bytes,
) -> bytes:
    """Build an encrypted risk score using only encrypted arithmetic.

    Mathematical model:
    - age is weighted by 1
    - glucose is weighted by 2
    - blood pressure is weighted by 2
    - bmi is weighted by 1
    - insulin is weighted by 1
    - raw risk score is the encrypted sum of the weighted inputs
    - thresholding compares the encrypted raw score against an encrypted threshold of 120
    - the comparison result is multiplied by an encrypted bonus of 10
    - the final score is the encrypted raw score plus the threshold bonus
    """

    age_ciphertext = _ensure_bytes(age_ciphertext, "age_ciphertext")
    glucose_ciphertext = _ensure_bytes(glucose_ciphertext, "glucose_ciphertext")
    blood_pressure_ciphertext = _ensure_bytes(blood_pressure_ciphertext, "blood_pressure_ciphertext")
    bmi_ciphertext = _ensure_bytes(bmi_ciphertext, "bmi_ciphertext")
    insulin_ciphertext = _ensure_bytes(insulin_ciphertext, "insulin_ciphertext")

    logger.info("Computing encrypted medical risk score from 5 encrypted inputs")

    weighted_age = engine.multiply(age_ciphertext, b"1")
    weighted_glucose = engine.multiply(glucose_ciphertext, b"2")
    weighted_blood_pressure = engine.multiply(blood_pressure_ciphertext, b"2")
    weighted_bmi = engine.multiply(bmi_ciphertext, b"1")
    weighted_insulin = engine.multiply(insulin_ciphertext, b"1")

    raw_score = engine.add(weighted_age, weighted_glucose)
    raw_score = engine.add(raw_score, weighted_blood_pressure)
    raw_score = engine.add(raw_score, weighted_bmi)
    raw_score = engine.add(raw_score, weighted_insulin)

    threshold_flag = engine.compare(raw_score, b"120")
    threshold_bonus = engine.multiply(threshold_flag, b"10")
    risk_score = engine.add(raw_score, threshold_bonus)

    return risk_score