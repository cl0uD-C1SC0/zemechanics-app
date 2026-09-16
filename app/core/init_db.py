from app.repositories import usuario_repository
from app.core.security import gerar_hash_senha
from app.database import SessionLocal
import os


def init_db():
    USER_NAME = os.getenv('USER_NAME', 'admin')
    USER_PASSWORD = os.getenv('USER_PASSWORD', 'admin123')
    db = SessionLocal()
    try:
        usuario = usuario_repository.get_usuario(USER_NAME, db)
        if not usuario:
            usuario_repository.criar_usuario(USER_NAME, gerar_hash_senha(USER_PASSWORD), db)
    finally:
        db.close()