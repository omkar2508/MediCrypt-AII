# Security Model

- The server only handles ciphertext, metadata, and audit records.
- The client owns the secret/private key material and never uploads it.
- Plaintext is only expected to exist on the trusted client before encryption and after local decryption.
- Audit logs should record sensitive operations without exposing secret material.
