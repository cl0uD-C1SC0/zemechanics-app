import pytest
from pydantic import ValidationError

from app.schemas.shared_schemas import ClienteResumo

def test_cliente_resumo_valido():
    data = {
        "id": 1,
        "nome": "José",
        "cpf": "12345678900"
    }

    result = ClienteResumo.model_validate(data)

    assert result.id == 1
    assert result.nome == "José"
    assert result.cpf == "12345678900"

def test_cliente_resumo_invalido():
    data = {
        "id": 1,
        "nome": "José"
    }

    with pytest.raises(ValidationError):
        ClienteResumo.model_validate(data)

def test_cliente_resumo_tipo_invalido():
    data = {
        "id": "errado",
        "nome": "José",
        "cpf": "123"
    }

    with pytest.raises(ValidationError):
        ClienteResumo.model_validate(data)

from unittest.mock import Mock

def test_cliente_resumo_from_attributes():
    obj = Mock()
    obj.id = 1
    obj.nome = "José"
    obj.cpf = "123"

    result = ClienteResumo.model_validate(obj)

    assert result.nome == "José"

