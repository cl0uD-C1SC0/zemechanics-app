from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import criar_token, verificar_senha, gerar_hash_senha
from app.repositories import usuario_repository
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
DB = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/auth", tags=["Auth"])

# TRANSFERIDO PARA FUNÇÃO LAMBDA
# @router.post("/login")
# def login(db: DB, form: OAuth2PasswordRequestForm = Depends()):
#     usuario = usuario_repository.get_usuario(form.username, db)
    
#     if not usuario or not verificar_senha(form.password, usuario.senha):
#         raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    
#     token = criar_token({"sub": usuario.username})
#     return {"access_token": token, "token_type": "bearer"}

# @router.post("/registrar", status_code=201)
# def registrar(db: DB, form: OAuth2PasswordRequestForm = Depends()):
#     if usuario_repository.get_usuario(form.username, db):
#         raise HTTPException(status_code=409, detail="Usuário já cadastrado")
    
#     novo_usuario = usuario_repository.criar_usuario(
#         form.username, 
#         gerar_hash_senha(form.password), 
#         db
#     )
#     return {"message": f"Usuário {novo_usuario.username} criado com sucesso"}