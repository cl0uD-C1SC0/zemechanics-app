from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

import os

BASE_DIR = os.getcwd()

dotenv = os.path.join(BASE_DIR, "../../env")



SECRET_KEY_JWT = str(os.getenv('SECRET_KEY_JWT')) 
ALGORITHM  = "HS256"
EXPIRES_IN = 60 

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def criar_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_IN)
    return jwt.encode(payload, SECRET_KEY_JWT, algorithm=ALGORITHM)

def verificar_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
    except JWTError:
        return None

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)