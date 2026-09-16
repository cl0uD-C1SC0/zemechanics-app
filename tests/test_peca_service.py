import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException

from app.services.peca_service import (
    adicionar_peca,
    listar_todas_pecas,
    consultar_peca_especifica,
    atualizar_peca_especifica,
    remover_peca,
    adicionar_ao_estoque,
    remover_do_estoque,
)

@patch("app.services.peca_service.PecaRepository")
def test_adicionar_peca_sucesso(mock_repo):
    db = Mock()

    peca = Mock()
    peca_salva = Mock()
    peca_salva.id = 1

    mock_repo.add_peca.return_value = peca_salva

    result = adicionar_peca(peca, db)

    assert "sucesso" in result["message"]

@patch("app.services.peca_service.PecaRepository")
def test_adicionar_peca_erro(mock_repo):
    db = Mock()
    peca = Mock()

    mock_repo.add_peca.return_value = None

    with pytest.raises(HTTPException) as exc:
        adicionar_peca(peca, db)

    assert exc.value.status_code == 500

@patch("app.services.peca_service.PecaRepository")
def test_listar_pecas_sucesso(mock_repo):
    db = Mock()

    mock_repo.get_all_pecas.return_value = [{"id": 1}]

    result = listar_todas_pecas(db)

    assert len(result) == 1

@patch("app.services.peca_service.PecaRepository")
def test_listar_pecas_vazio(mock_repo):
    db = Mock()

    mock_repo.get_all_pecas.return_value = []

    with pytest.raises(HTTPException) as exc:
        listar_todas_pecas(db)

    assert exc.value.status_code == 404

@patch("app.services.peca_service.PecaRepository")
def test_consultar_peca_sucesso(mock_repo):
    db = Mock()

    mock_repo.describe_peca.return_value = {"id": 1}

    result = consultar_peca_especifica(1, db)

    assert result["id"] == 1

@patch("app.services.peca_service.PecaRepository")
def test_consultar_peca_nao_encontrada(mock_repo):
    db = Mock()

    mock_repo.describe_peca.return_value = None

    with pytest.raises(HTTPException) as exc:
        consultar_peca_especifica(1, db)

    assert exc.value.status_code == 404

@patch("app.services.peca_service.PecaRepository")
def test_atualizar_peca_sucesso(mock_repo):
    db = Mock()

    mock_repo.describe_peca.return_value = {"id": 1}
    mock_repo.update_peca.return_value = True

    result = atualizar_peca_especifica(1, {"nome": "nova"}, db)

    assert "atualizada" in result["message"]

@patch("app.services.peca_service.PecaRepository")
def test_atualizar_peca_nao_encontrada(mock_repo):
    db = Mock()

    mock_repo.describe_peca.return_value = None

    with pytest.raises(HTTPException) as exc:
        atualizar_peca_especifica(1, {}, db)

    assert exc.value.status_code == 404

@patch("app.services.peca_service.PecaRepository")
def test_remover_peca_sucesso(mock_repo):
    db = Mock()

    mock_repo.describe_peca.return_value = True
    mock_repo.delete_peca.return_value = True

    result = remover_peca(1, db)

    assert "sucesso" in result["message"]

@patch("app.services.peca_service.PecaRepository")
def test_remover_peca_nao_encontrada(mock_repo):
    db = Mock()

    mock_repo.describe_peca.return_value = None

    with pytest.raises(HTTPException) as exc:
        remover_peca(1, db)

    assert exc.value.status_code == 404

@patch("app.services.peca_service.PecaRepository")
def test_adicionar_estoque_sucesso(mock_repo):
    db = Mock()

    peca = Mock()
    peca.nome = "Motor"

    mock_repo.describe_peca.return_value = peca
    mock_repo.add_peca_amount.return_value = True

    result = adicionar_ao_estoque(1, 5, db)

    assert "Adicionado" in result["message"]

@patch("app.services.peca_service.PecaRepository")
def test_adicionar_estoque_erro(mock_repo):
    db = Mock()

    peca = Mock()
    mock_repo.describe_peca.return_value = peca
    mock_repo.add_peca_amount.return_value = None

    with pytest.raises(HTTPException) as exc:
        adicionar_ao_estoque(1, 5, db)

    assert exc.value.status_code == 500

@patch("app.services.peca_service.PecaRepository")
def test_remover_estoque_sucesso(mock_repo):
    db = Mock()

    peca = Mock()
    peca.nome = "Motor"

    mock_repo.describe_peca.return_value = peca
    mock_repo.remove_peca_amount.return_value = True

    result = remover_do_estoque(1, 2, db)

    assert "Removido" in result["message"]

@patch("app.services.peca_service.PecaRepository")
def test_remover_estoque_erro(mock_repo):
    db = Mock()

    peca = Mock()
    mock_repo.describe_peca.return_value = peca
    mock_repo.remove_peca_amount.return_value = None

    with pytest.raises(HTTPException) as exc:
        remover_do_estoque(1, 2, db)

    assert exc.value.status_code == 500