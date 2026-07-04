from app.services.audit_service import AuditService


if __name__ == "__main__":
    audit_service = AuditService()
    audit_service.record_event("seed_demo_data", actor="system")
    print("seeded demo data")
