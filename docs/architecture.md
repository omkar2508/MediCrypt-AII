# Architecture

This repository is organized into two Python applications:

- `server/` hosts the FastAPI service, persistence layer, logging, security middleware, and the FHE compute core.
- `client/` holds the trusted-device workflow for key generation, local encryption, API calls, and local decryption.

The code is structured so that FHE-specific logic lives under `server/app/fhe_compute/` and remains isolated from FastAPI route code.
