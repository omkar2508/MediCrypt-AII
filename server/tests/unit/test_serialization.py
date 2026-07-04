from app.fhe_compute.serialization import deserialize_ciphertext, serialize_ciphertext


def test_round_trip_ciphertext() -> None:
    payload = b"ciphertext"
    encoded = serialize_ciphertext(payload)
    assert deserialize_ciphertext(encoded) == payload
