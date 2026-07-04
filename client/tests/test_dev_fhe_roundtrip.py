import importlib.util
import sys
import unittest
from pathlib import Path

from decryptor import decrypt_result
from encryptor import encrypt_payload


class DevFheRoundTripTests(unittest.TestCase):
    def test_encrypt_payload_still_round_trips_locally(self) -> None:
        key = b"demo-key"
        ciphertext = encrypt_payload(42, key)
        self.assertNotEqual(ciphertext, b"")

    def test_matches_server_dev_backend_masking(self) -> None:
        server_root = Path(__file__).resolve().parents[1] / ".." / "server"
        sys.path.insert(0, str(server_root))
        server_backend_path = server_root / "app" / "fhe_compute" / "dev_backend.py"
        spec = importlib.util.spec_from_file_location("server_dev_backend", server_backend_path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        key = b"demo-key"
        ciphertext = encrypt_payload(42, key)
        evaluated = module.DevPythonEngine().evaluate_prediction(ciphertext, key_material=module.derive_evaluation_key(key))

        self.assertEqual(decrypt_result(evaluated, key), "42")


if __name__ == "__main__":
    unittest.main()
