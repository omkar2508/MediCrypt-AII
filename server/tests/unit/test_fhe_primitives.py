from app.fhe_compute.primitives.encrypted_add import encrypted_add
from app.fhe_compute.primitives.encrypted_compare import encrypted_compare
from app.fhe_compute.primitives.encrypted_multiply import encrypted_multiply


def test_encrypted_add() -> None:
    assert encrypted_add(b"a", b"b") == b"add:a:b"


def test_encrypted_multiply() -> None:
    assert encrypted_multiply(b"a", b"b") == b"multiply:a:b"


def test_encrypted_compare() -> None:
    assert encrypted_compare(b"a", b"b") == b"compare:a:b"
