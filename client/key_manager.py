from dataclasses import dataclass
import json
import logging
from pathlib import Path
from uuid import uuid4


logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ClientKeyPair:
    key_id: str
    key_dir: Path
    manifest_path: Path


class KeyManager:
    def __init__(self, key_dir: Path | None = None) -> None:
        self.key_dir = key_dir or Path(__file__).with_name("keys")
        self.key_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_path = self.key_dir / "keypair.json"

    def load_or_create_keys(self) -> ClientKeyPair:
        if self._manifest_path.exists():
            return self._load_existing_keypair()

        key_id = str(uuid4())
        payload = {"key_id": key_id}
        self._manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        logger.info("Created new client keypair manifest at %s", self._manifest_path)
        return ClientKeyPair(key_id=key_id, key_dir=self.key_dir, manifest_path=self._manifest_path)

    def _load_existing_keypair(self) -> ClientKeyPair:
        try:
            raw_manifest = self._manifest_path.read_text(encoding="utf-8")
            payload = json.loads(raw_manifest)
            key_id = str(payload["key_id"])
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Invalid client keypair manifest: {self._manifest_path}") from exc

        logger.info("Loaded existing client keypair manifest from %s", self._manifest_path)
        return ClientKeyPair(key_id=key_id, key_dir=self.key_dir, manifest_path=self._manifest_path)
