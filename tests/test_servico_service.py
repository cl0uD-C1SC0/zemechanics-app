import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException

from app.services.servico_service import (
    adicionar_servico,
    listar_todos_servicos,
    consultar_servico_especifico,
    atualizar_servico_especifico,
    remover_servico,
)

@patch("app.services.servico_service.ServicosRepository")
def test_adicionar_servico_sucesso(mock_repo):
    db = Mock()

    servico = Mock()
    servico_salvo = Mock()
    servico_salvo.id = 1

    mock_repo.add_mechanic_service.return_value = servico_salvo

    result = adicionar_servico(servico, db)

    assert "sucesso" in result["message"]

@patch("app.services.servico_service.ServicosRepository")
def test_adicionar_servico_erro(mock_repo):
    db = Mock()
    servico = Mock()

    mock_repo.add_mechanic_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        adicionar_servico(servico, db)

    assert exc.value.status_code == 500

@patch("app.services.servico_service.ServicosRepository")
def test_listar_servicos_sucesso(mock_repo):
    db = Mock()

    mock_repo.get_all_services.return_value = [{"id": 1}]

    result = listar_todos_servicos(db)

    assert len(result) == 1

@patch("app.services.servico_service.ServicosRepository")
def test_listar_servicos_vazio(mock_repo):
    db = Mock()

    mock_repo.get_all_services.return_value = []

    with pytest.raises(HTTPException) as exc:
        listar_todos_servicos(db)

    assert exc.value.status_code == 404

@patch("app.services.servico_service.ServicosRepository")
def test_consultar_servico_sucesso(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = {"id": 1}

    result = consultar_servico_especifico(1, db)

    assert result["id"] == 1

@patch("app.services.servico_service.ServicosRepository")
def test_consultar_servico_nao_encontrado(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        consultar_servico_especifico(1, db)

    assert exc.value.status_code == 404

@patch("app.services.servico_service.ServicosRepository")
def test_atualizar_servico_sucesso(mock_repo):
    db = Mock()

    servico = Mock()
    servico.id = 1

    mock_repo.describe_service.return_value = servico
    mock_repo.update_service.return_value = servico

    result = atualizar_servico_especifico(1, {"nome": "novo"}, db)

    assert "atualizado com sucesso" in result["message"]

@patch("app.services.servico_service.ServicosRepository")
def test_atualizar_servico_nao_encontrado(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        atualizar_servico_especifico(1, {}, db)

    assert exc.value.status_code == 404

@patch("app.services.servico_service.ServicosRepository")
def test_atualizar_servico_erro(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = {"id": 1}
    mock_repo.update_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        atualizar_servico_especifico(1, {}, db)

    assert exc.value.status_code == 500

@patch("app.services.servico_service.ServicosRepository")
def test_remover_servico_sucesso(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = True
    mock_repo.delete_service.return_value = True

    result = remover_servico(1, db)

    assert "sucesso" in result["message"]

@patch("app.services.servico_service.ServicosRepository")
def test_remover_servico_nao_encontrado(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        remover_servico(1, db)

    assert exc.value.status_code == 404

@patch("app.services.servico_service.ServicosRepository")
def test_remover_servico_erro(mock_repo):
    db = Mock()

    mock_repo.describe_service.return_value = True
    mock_repo.delete_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        remover_servico(1, db)

    assert exc.value.status_code == 500