import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.OrdemServicoSchema import (
    OrdemDeServicoSchema,
    OSUpdateSchema,
    OSResponse,
)

def test_ordem_servico_schema_valido():
    data = {
        "cliente_cpf": 123,
        "veiculo_placa": "ABC1234"
    }

    os = OrdemDeServicoSchema(**data)

    assert os.cliente_cpf == 123
    assert os.veiculo_placa == "ABC1234"

def test_ordem_servico_schema_invalido():
    data = {
        "cliente_cpf": "errado" 
    }

    with pytest.raises(ValidationError):
        OrdemDeServicoSchema(**data)

def test_os_update_schema_parcial():
    data = {
        "cliente_cpf": 999
    }

    os = OSUpdateSchema(**data)

    assert os.cliente_cpf == 999
    assert os.veiculo_placa is None

def test_os_update_schema_dump():
    data = {
        "cliente_cpf": 123,
        "veiculo_placa": None
    }

    os = OSUpdateSchema(**data)

    result = os.model_dump(exclude_none=True)

    assert "cliente_cpf" in result
    assert "veiculo_placa" not in result

def test_os_response_valido():
    data = {
        "id": 1,
        "status": "EM_EXECUCAO",
        "criado_em": datetime.now(),
        "cliente": {
            "id": 1,
            "nome": "José",
            "cpf": "123"
        },
        "veiculo": {
            "id": 1,
            "marca": "Honda",
            "modelo": "Civic",
            "placa": "ABC1234"
        }
    }

    result = OSResponse.model_validate(data)

    assert result.id == 1
    assert result.cliente.nome == "José"
    assert result.veiculo.modelo == "Civic"

def test_os_response_invalido():
    data = {
        "id": 1,
        "status": "OK",
        "criado_em": datetime.now(),
        "cliente": {
            "id": 1
            # faltando campos
        },
        "veiculo": {}
    }

    with pytest.raises(ValidationError):
        OSResponse.model_validate(data)
