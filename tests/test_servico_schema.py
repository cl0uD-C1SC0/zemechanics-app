import pytest
from pydantic import ValidationError

from app.schemas.Servico import (
    ServicoSchema,
    UpdateServiceSchema,
    ServicoResponse,
    ConsultAllServicosSchema,
)

def test_servico_schema_valido():
    data = {
        "nome": "Troca de óleo",
        "preco": 120.0,
        "descricao": "Troca completa"
    }

    servico = ServicoSchema(**data)

    assert servico.nome == "Troca de óleo"
    assert servico.preco == 120.0

def test_servico_schema_invalido():
    data = {
        "nome": "Teste"
    }

    with pytest.raises(ValidationError):
        ServicoSchema(**data)

def test_update_service_schema_parcial():
    data = {
        "nome": "Novo Nome"
    }

    servico = UpdateServiceSchema(**data)

    assert servico.nome == "Novo Nome"
    assert servico.preco is None

def test_update_service_schema_dump():
    data = {
        "nome": "Atualizado",
        "descricao": None
    }

    servico = UpdateServiceSchema(**data)

    result = servico.model_dump(exclude_none=True)

    assert "nome" in result
    assert "descricao" not in result

def test_servico_response_valido():
    data = {
        "id": 1,
        "nome": "Diagnóstico",
        "preco": 80.0
    }

    result = ServicoResponse.model_validate(data)

    assert result.id == 1
    assert result.nome == "Diagnóstico"

def test_servico_response_invalido():
    data = {
        "id": 1,
        "nome": "Erro"
    }

    with pytest.raises(ValidationError):
        ServicoResponse.model_validate(data)

def test_consult_all_servicos_schema():
    data = {
        "id": 1,
        "nome": "Troca de óleo"
    }

    result = ConsultAllServicosSchema.model_validate(data)

    assert result.id == 1
    assert result.nome == "Troca de óleo"