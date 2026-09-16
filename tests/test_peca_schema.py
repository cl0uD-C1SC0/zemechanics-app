import pytest
from pydantic import ValidationError

from app.schemas.Peca import (
    PecaSchema,
    UpdatePecaSchema,
    PecaResponse,
    ConsultAllPecasSchema,
)

def test_peca_schema_valido():
    data = {
        "nome": "Filtro",
        "preco": 50.0,
        "quantidade": 10
    }

    peca = PecaSchema(**data)

    assert peca.nome == "Filtro"
    assert peca.preco == 50.0

def test_peca_schema_invalido():
    data = {
        "nome": "Filtro"
        # faltando campos obrigatórios
    }

    with pytest.raises(ValidationError):
        PecaSchema(**data)

def test_update_peca_schema_parcial():
    data = {
        "nome": "Novo Nome"
    }

    peca = UpdatePecaSchema(**data)

    assert peca.nome == "Novo Nome"
    assert peca.preco is None

def test_update_peca_schema_dump():
    data = {
        "nome": "Atualizado",
        "preco": None
    }

    peca = UpdatePecaSchema(**data)

    result = peca.model_dump(exclude_none=True)

    assert "nome" in result
    assert "preco" not in result

def test_peca_response_valido():
    data = {
        "id": 1,
        "nome": "Motor",
        "preco": 500.0,
        "quantidade": 2
    }

    result = PecaResponse.model_validate(data)

    assert result.id == 1
    assert result.nome == "Motor"

def test_peca_response_invalido():
    data = {
        "id": 1,
        "nome": "Motor"
        # faltando preco e quantidade
    }

    with pytest.raises(ValidationError):
        PecaResponse.model_validate(data)

def test_consult_all_pecas_schema():
    data = {
        "id": 1,
        "nome": "Filtro"
    }

    result = ConsultAllPecasSchema.model_validate(data)

    assert result.id == 1
    assert result.nome == "Filtro"