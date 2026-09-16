from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def verificar_liveness():
    return {"status": "ok"}


def verificar_readiness(db):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return False
    return True
