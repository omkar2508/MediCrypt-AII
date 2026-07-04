from abc import ABC, abstractmethod


class EncryptedComputeEngine(ABC):
    @abstractmethod
    def add(self, left: bytes, right: bytes) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def multiply(self, left: bytes, right: bytes) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def compare(self, left: bytes, right: bytes) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def score(self, values: list[bytes]) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def evaluate_prediction(self, ciphertext: bytes, key_material: bytes | None = None) -> bytes:
        raise NotImplementedError
