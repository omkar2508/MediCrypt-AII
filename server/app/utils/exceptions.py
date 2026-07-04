class MedicryptError(Exception):
    """Base application error."""


class CiphertextCorruptedError(MedicryptError):
    """Raised when ciphertext cannot be recovered or decoded."""


class UnauthorizedKeyAccessError(MedicryptError):
    """Raised when a key handle does not match the request context."""
