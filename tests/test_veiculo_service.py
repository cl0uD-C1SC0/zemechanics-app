import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException

from app.services.veiculo_service import (
    cadastrar_veiculo,
    consultar_veiculo,
    atualizar_dados_veiculo,
    listar_todos_veiculos,
    remover_veiculo,
)

@patch("app.services.veiculo_service.VeiculoRepository")
def test_cadastrar_veiculo_sucesso(mock_repo):
    veiculo = Mock()
    veiculo.placa = "ABC1234"

    db = Mock()

    mock_repo.get_vehicle.return_value = None

    veiculo_salvo = Mock()
    veiculo_salvo.id = 1
    mock_repo.add_veiculo.return_value = veiculo_salvo

    result = cadastrar_veiculo(veiculo, db)

    assert "Veiculo cadastrado com sucesso" in result["message"]
    mock_repo.add_veiculo.assert_called_once()

@patch("app.services.veiculo_service.VeiculoRepository")
def test_cadastrar_veiculo_placa_existente(mock_repo):
    veiculo = Mock()
    veiculo.placa = "ABC1234"
    db = Mock()

    mock_repo.get_vehicle.return_value = True

    with pytest.raises(HTTPException) as exc:
        cadastrar_veiculo(veiculo, db)

    assert exc.value.status_code == 409

@patch("app.services.veiculo_service.VeiculoRepository")
def test_cadastrar_veiculo_erro_salvar(mock_repo):
    veiculo = Mock()
    veiculo.placa = "ABC1234"
    db = Mock()

    mock_repo.get_vehicle.return_value = None
    mock_repo.add_veiculo.return_value = None

    with pytest.raises(HTTPException) as exc:
        cadastrar_veiculo(veiculo, db)

    assert exc.value.status_code == 500

@patch("app.services.veiculo_service.VeiculoRepository")
def test_consultar_veiculo_sucesso(mock_repo):
    db = Mock()
    mock_repo.get_vehicle.return_value = {"placa": "ABC1234"}

    result = consultar_veiculo("ABC1234", db)

    assert result["placa"] == "ABC1234"

@patch("app.services.veiculo_service.VeiculoRepository")
def test_consultar_veiculo_nao_encontrado(mock_repo):
    db = Mock()
    mock_repo.get_vehicle.return_value = None

    with pytest.raises(HTTPException) as exc:
        consultar_veiculo("ABC1234", db)

    assert exc.value.status_code == 404

@patch("app.services.veiculo_service.VeiculoRepository")
def test_atualizar_veiculo_sucesso(mock_repo):
    db = Mock()

    mock_repo.get_vehicle.return_value = {"placa": "ABC1234"}
    mock_repo.update_vehicle_info.return_value = True

    result = atualizar_dados_veiculo("ABC1234", {"cor": "preto"}, db)

    assert "atualizados" in result["message"]

@patch("app.services.veiculo_service.VeiculoRepository")
def test_atualizar_veiculo_nao_encontrado(mock_repo):
    db = Mock()
    mock_repo.get_vehicle.return_value = None

    with pytest.raises(HTTPException) as exc:
        atualizar_dados_veiculo("ABC1234", {}, db)

    assert exc.value.status_code == 404

@patch("app.services.veiculo_service.VeiculoRepository")
def test_listar_veiculos_sucesso(mock_repo):
    db = Mock()
    mock_repo.get_all_vehicles.return_value = [{"placa": "ABC"}]

    result = listar_todos_veiculos(db)

    assert len(result) == 1

@patch("app.services.veiculo_service.VeiculoRepository")
def test_listar_veiculos_vazio(mock_repo):
    db = Mock()
    mock_repo.get_all_vehicles.return_value = []

    with pytest.raises(HTTPException) as exc:
        listar_todos_veiculos(db)

    assert exc.value.status_code == 404

@patch("app.services.veiculo_service.VeiculoRepository")
def test_remover_veiculo_sucesso(mock_repo):
    db = Mock()

    mock_repo.get_vehicle.return_value = True
    mock_repo.delete_vehicle.return_value = True

    result = remover_veiculo("ABC1234", db)

    assert "sucesso" in result["message"]

@patch("app.services.veiculo_service.VeiculoRepository")
def test_remover_veiculo_nao_encontrado(mock_repo):
    db = Mock()
    mock_repo.get_vehicle.return_value = None

    with pytest.raises(HTTPException) as exc:
        remover_veiculo("ABC1234", db)

    assert exc.value.status_code == 404