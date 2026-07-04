from sqlalchemy import text
from app.db.session import engine
import logging

logger = logging.getLogger(__name__)

CREATE_PUBLIC_EVAL_KEY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS public_evaluation_keys (
  id VARCHAR(36) PRIMARY KEY,
  owner_id VARCHAR(36) NOT NULL,
  key_id VARCHAR(128) NOT NULL UNIQUE,
  key_material VARCHAR(2048) NOT NULL,
  version VARCHAR(50) NOT NULL DEFAULT 'v1',
  revoked BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_INDEX_OWNER_ID = """
CREATE INDEX IF NOT EXISTS idx_public_eval_keys_owner ON public_evaluation_keys (owner_id);
"""


def ensure_public_evaluation_keys_table() -> None:
    """Create the public_evaluation_keys table if it does not exist."""
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_PUBLIC_EVAL_KEY_TABLE_SQL))
            conn.execute(text(CREATE_INDEX_OWNER_ID))
        logger.info("Ensured public_evaluation_keys table exists")
    except Exception:
        logger.exception("Failed to ensure public_evaluation_keys table exists")
        raise
