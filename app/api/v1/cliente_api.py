from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.services import cliente_service
from app.schemas.cliente_schema import ClienteSchema, ConsultAllClientsResponse, ClienteUpdateSchema, ConsultClientResponse

router = APIRouter(prefix="/cliente", tags=["Clientes v1"])
DB = Annotated[Session, Depends(get_db)]

@router.post("/novo_cliente", status_code=status.HTTP_201_CREATED, summary="CADASTRAR NOVO CLIENTE", description="Cadastra um novo cliente com CPF, Nome, Endereco & Contato")
def cadastrar_cliente(cliente: ClienteSchema, db: DB):
    novo_cliente = cliente_service.cadastrar_cliente(cliente, db)
    return novo_cliente

@router.get("/clientes", response_model=list[ConsultAllClientsResponse], summary="LISTAR TODOS OS CLIENTES", description="Lista todas as informações, incluindo o ID dos clientes")
def listar_clientes(db: DB):
    clientes = cliente_service.listar_clientes(db)
    return clientes

@router.get("/{cpf}", response_model=ConsultClientResponse, summary="CONSULTAR UM CLIENTE", description="Consultar todos os dados de um cliente com base em um CPF")
def consultar_cliente(cpf: int, db: DB):
    cliente = cliente_service.consultar_cliente(cpf, db)    
    return cliente

@router.get("/{cpf}/veiculos", summary="LISTAR APENAS OS VEÍCULOS DO CLIENTE", description="Consulta todos os veículos do cliente que foram cadastrados")
def listar_veiculos_do_cliente(cpf: int, db: DB):
    cliente_veiculos = cliente_service.listar_veiculos_cliente(cpf, db)
    return cliente_veiculos

@router.patch("/{cpf}/atualizar_informacoes", summary="ATUALIZAR DADOS DO CLIENTE", description="Atualizar dados como NOME, CONTATO, ENDERECO")
def atualizar_cliente(cpf: int, dados: ClienteUpdateSchema, db: DB):
    dados_atualizados = cliente_service.atualizar_informacao_cliente(cpf, dados, db)
    return dados_atualizados

@router.patch("/{novo_cpf}/transferir_veiculo/{placa}", summary="TRANSFERIR VEÍCULO À OUTRO CPF", description="Transferir um veículo para um novo CPF")
def transferir_veiculo(novo_cpf: int, placa: str, db: DB):
    veiculo_transferido = cliente_service.transferir_veiculo_cliente(placa, novo_cpf, db)
    return veiculo_transferido

@router.delete("/{cpf}/remover_cliente", summary="REMOVER UM CLIENTE", description="Remover um cliente que foi cadastrado")
def remover_cliente(cpf: int, db: DB):
    cliente_removido = cliente_service.remover_cliente(cpf, db)
    return cliente_removido