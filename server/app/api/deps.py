from typing import Generator

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.audit_service import AuditService
from app.services.auth_service import AuthService
from app.services.encryption_service import EncryptionService
from app.services.medical_service import MedicalService
from app.services.ml_service import MLService
from app.services.prediction_service import PredictionService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request) -> str:
    token_payload = getattr(request.state, "token_payload", None)
    if not token_payload or "sub" not in token_payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return str(token_payload["sub"])


def get_auth_service() -> AuthService:
    return AuthService()


def get_encryption_service(db: Session = Depends(get_db)) -> EncryptionService:
    return EncryptionService(db)


def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(db)


def get_prediction_service(db: Session = Depends(get_db), audit_service: AuditService = Depends(get_audit_service), encryption_service: EncryptionService = Depends(get_encryption_service)) -> PredictionService:
    return PredictionService(db=db, audit_service=audit_service, encryption_service=encryption_service)


def get_medical_service(db: Session = Depends(get_db), audit_service: AuditService = Depends(get_audit_service)) -> MedicalService:
    return MedicalService(db=db, audit_service=audit_service)


def get_ml_service(db: Session = Depends(get_db), audit_service: AuditService = Depends(get_audit_service)) -> MLService:
    return MLService()
