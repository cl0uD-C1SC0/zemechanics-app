from fastapi import APIRouter, Depends, Query, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.OrdemServicoSchema import OrdemDeServicoSchema, OSUpdateSchema, OSResponse, OSCompletaSchema
from app.services import OSService as os_service

router = APIRouter(prefix="/ordem_servico", tags=["OrdemDeServico"])
DB = Annotated[Session, Depends(get_db)]

@router.post("/nova_os", status_code=status.HTTP_201_CREATED, summary="CADASTRAR UMA NOVA OS", description="Cria uma nova OS com apenas um veículo atribuído por vez")
def criar_os(os: OrdemDeServicoSchema, db: DB):
    nova_os = os_service.criar_nova_os(os, db)
    return nova_os

@router.post("/nova_os_completa", status_code=status.HTTP_201_CREATED, summary="CADASTRAR UMA OS COMPLETA", description="Cadastra cliente, veículo e cria a OS em uma única chamada, associando peças e serviços já cadastrados no sistema")
def criar_os_completa(dados: OSCompletaSchema, db: DB):
    nova_os_completa = os_service.criar_os_completa(dados, db)
    return nova_os_completa

@router.get("/consultar/{os_id}", summary="CONSULTAR UMA OS", description="Consultar todas as informações de uma OS")
def consultar_ordemservico(os_id: int, db: DB):
    os_consultada = os_service.consultar_os(os_id, db)
    return os_consultada

@router.post("/{os_id}/adicionar_peca/{peca_id}", summary="ADICIONAR UMA PEÇA/INSUMO NA OS", description="Adicionar uma peça pelo ID e sua quantidade na OS")
def adicionar_peca_os(os_id: int, peca_id: int, db: DB, quantidade: int = Query(..., ge=1)):
    resultado = os_service.adicionar_peca_os(os_id, peca_id, quantidade, db)
    return resultado

@router.post("/{os_id}/adicionar_servico/{servico_id}", summary="ADICIONAR UM SERVIÇO/MÃO DE OBRA NA OS", description="Adicionar um serviço pelo ID na OS")
def adicionar_servico_os(os_id: int, servico_id: int, db: DB):
    resultado = os_service.adicionar_servico_os(os_id, servico_id, db)
    return resultado

@router.post("/confirmar_aprovacao/{os_id}", summary="CONFIRMAR APROVAÇÃO DA OS", description="Confirmar a aprovação de uma OS")
def aprovar_os(os_id: int, db: DB, cliente_cpf: str = Query(...)):
    return os_service.aprovar_os(os_id, cliente_cpf, db)

@router.post("/reprovar/{os_id}", summary="REPROVAR ORÇAMENTO DA OS", description="Recusar o orçamento de uma OS, encerrando-a definitivamente com o status Reprovada")
def reprovar_os(os_id: int, db: DB, cliente_cpf: str = Query(...)):
    return os_service.reprovar_os(os_id, cliente_cpf, db)

@router.patch("/avancar/{os_id}", summary="AVANÇAR STATUS DA OS", description="Avançar os status de uma OS")
def avancar_ordem(os_id: int, db: DB):
    os_avancada = os_service.avancar_os(os_id, db)
    return os_avancada

@router.patch("/atualizar/{os_id}", summary="ATUALIZAR CPF OU VEÍCULO DA OS", description="Atualiza o CPF ou o veiculo da OS")
def atualizar_os(os_id: int, dados: OSUpdateSchema, db: DB):
    os_atualizada = os_service.atualizar_os(os_id, dados, db)
    return os_atualizada

@router.get("/ordens", response_model=list[OSResponse], summary="LISTAR TODAS AS ORDENS", description="Listar todas as ordens criadas no sistema, seu ID, cliente e o veículo")
def listar_todas_as_os(db: DB):
    ordens = os_service.listar_todas_os(db)
    return ordens

@router.get("/aprovar/{os_id}", summary="APROVAR UMA OS", description="Aprovar uma Ordem de serviço quando estiver com Status = 'AGUARDANDO APROVAÇÃO'")
def pagina_aprovacao(os_id: int, db: DB, cliente_cpf: str = Query(...)):
    dados_os = os_service.consultar_os(os_id, db)
    os_pagina_aprovacao = os_service._mostrar_aprovacao(os_id, dados_os, cliente_cpf)

    return os_pagina_aprovacao

@router.delete("/{os_id}/remover_peca/{peca_id}", summary="REMOVER UMA PEÇA DA OS", description="Remover uma peça adicionada na OS")
def remover_peca_os(os_id: int, peca_id: int, db: DB):
    resultado = os_service.remover_peca_os(os_id, peca_id, db)
    return resultado

@router.delete("/{os_id}/remover_servico/{servico_id}", summary="REMOVER UM SERVICO DA OS", description="Remover um serviço adicionado na OS")
def remover_servico_os(os_id: int, servico_id: int, db: DB):
    resultado = os_service.remover_servico_os(os_id, servico_id, db)
    return resultado

@router.delete("/excluir/{os_id}", summary="EXCLUIR UMA OS", description="Remover uma OS criada do sistema")
def excluir_os(os_id: int, db: DB):
    os_removida = os_service.remover_os(os_id, db)
    return os_removida