from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.schemas.Servico import ServicoSchema, UpdateServiceSchema, ConsultAllServicosSchema
from app.services import servico_service as servico_service

router = APIRouter(prefix="/servico", tags=["Serviços v1"])
DB = Annotated[Session, Depends(get_db)]

@router.post("/adicionar_servico", status_code=status.HTTP_201_CREATED, summary="CADASTRAR UM NOVO SERVIÇO", description="Adiciona um novo serviço/mão de obra no sistema")                                   
def cadastrar_servico(servico: ServicoSchema, db: DB):  
    novo_servico = servico_service.adicionar_servico(servico, db)
    return novo_servico

@router.get("/servicos", response_model=list[ConsultAllServicosSchema], summary="LISTAR TODOS OS SERVIÇOS", description="Lista todos os serviços cadastrados no sistema")
def listar_servicos(db: DB):
    servicos = servico_service.listar_todos_servicos(db)
    return servicos

@router.get("/consultar_servico/{servico_id}", summary="CONSULTAR SERVIÇO ESPECÍFICO", description="Consulta um serviço específico com base no ID do Serviço")
def consultar_servico(servico_id: int, db: DB):
    servico = servico_service.consultar_servico_especifico(servico_id, db)
    return servico

@router.patch("/atualizar_servico/{servico_id}", summary="ATUALIZAR INFORMAÇÕES DO SERVIÇO", description="Atualiza informações do serviço: NOME, PREÇO & DESCRIÇÃO")
def atualizar_servico(servico_id: int, dados: UpdateServiceSchema, db: DB):
    servico_atualizado = servico_service.atualizar_servico_especifico(servico_id, dados, db)
    return servico_atualizado

@router.delete("/remover_servico/{servico_id}", summary="REMOVER UM SERVIÇO", description="Remove do sistema um serviço cadastrado")
def remover_servico(servico_id: int, db: DB):
    servico_removido = servico_service.remover_servico(servico_id, db)
    return servico_removido