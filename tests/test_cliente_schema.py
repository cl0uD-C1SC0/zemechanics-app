import pytest
from pydantic import ValidationError

from app.schemas.cliente_schema import (
    ClienteSchema,
    ClienteUpdateSchema,
    ConsultAllClientsResponse,
    ConsultClientResponse,
)

def test_cliente_schema_valido():
    data = {
        "nome": "José",
        "cpf": "123",
        "endereco": "Rua A",
        "telefone": "999",
        "email": "jose@email.com"
    }

    cliente = ClienteSchema(**data)

    assert cliente.nome == "José"
    assert cliente.cpf == "123"

def test_cliente_schema_invalido():
    data = {
        "nome": "José"
        # faltando campos obrigatórios
    }

    with pytest.raises(ValidationError):
        ClienteSchema(**data)

def test_cliente_update_schema_parcial():
    data = {
        "nome": "Novo Nome"
    }

    cliente = ClienteUpdateSchema(**data)

    assert cliente.nome == "Novo Nome"
    assert cliente.email is None

def test_cliente_update_model_dump():
    data = {
        "nome": "Atualizado",
        "email": None
    }

    cliente = ClienteUpdateSchema(**data)

    result = cliente.model_dump(exclude_none=True)

    assert "nome" in result
    assert "email" not in result

def test_consult_all_clients_response():
    obj = Mock()
    obj.id = 1
    obj.nome = "José"

    result = ConsultAllClientsResponse.model_validate(obj)

    assert result.id == 1
    assert result.nome == "José"

from unittest.mock import Mock

def test_consult_client_response_sem_veiculos():
    obj = Mock()
    obj.id = 1
    obj.nome = "José"
    obj.cpf = "123"
    obj.telefone = "999"
    obj.email = "jose@email.com"
    obj.endereco = "Rua A"
    obj.veiculos = []

    result = ConsultClientResponse.model_validate(obj)

    assert result.nome == "José"
    assert result.veiculos == []

def test_consult_client_response_com_veiculos():
    cliente_veiculo = Mock()
    cliente_veiculo.id = 1
    cliente_veiculo.nome = "José"
    cliente_veiculo.cpf = "123"

    veiculo = Mock()
    veiculo.id = 1
    veiculo.placa = "ABC123"
    veiculo.marca = "Honda"
    veiculo.modelo = "Civic"
    veiculo.ano = "2020"
    veiculo.cliente = cliente_veiculo

    cliente = Mock()
    cliente.id = 1
    cliente.nome = "José"
    cliente.cpf = "123"
    cliente.telefone = "999"
    cliente.email = "jose@email.com"
    cliente.endereco = "Rua A"
    cliente.veiculos = [veiculo]

    result = ConsultClientResponse.model_validate(cliente)

    assert len(result.veiculos) == 1
    assert result.veiculos[0].marca == "Honda"