from unittest.mock import Mock

from app.repositories.VeiculoRepository import (
    add_veiculo,
    get_vehicle,
    get_all_vehicles,
    update_vehicle_info,
    delete_vehicle,
)

def test_add_veiculo(db):
    veiculo = Mock()
    veiculo.modelo = "Civic"
    veiculo.marca = "Honda"
    veiculo.placa = "ABC1234"
    veiculo.ano = 2020
    veiculo.cliente_id = 1

    result = add_veiculo(veiculo, db)

    assert result.id is not None
    assert result.placa == "ABC1234"

def test_get_vehicle(db):
    veiculo = Mock()
    veiculo.modelo = "Gol"
    veiculo.marca = "VW"
    veiculo.placa = "XYZ9999"
    veiculo.ano = 2015
    veiculo.cliente_id = 1

    add_veiculo(veiculo, db)

    result = get_vehicle("XYZ9999", db)

    assert result is not None
    assert result.modelo == "Gol"

def test_get_all_vehicles(db):
    v1 = Mock()
    v1.modelo = "A"
    v1.marca = "X"
    v1.placa = "111"
    v1.ano = 2010
    v1.cliente_id = 1

    v2 = Mock()
    v2.modelo = "B"
    v2.marca = "Y"
    v2.placa = "222"
    v2.ano = 2020
    v2.cliente_id = 2

    add_veiculo(v1, db)
    add_veiculo(v2, db)

    result = get_all_vehicles(db)

    assert len(result) == 2

def test_update_vehicle_info(db):
    veiculo = Mock()
    veiculo.modelo = "Uno"
    veiculo.marca = "Fiat"
    veiculo.placa = "UPD123"
    veiculo.ano = 2010
    veiculo.cliente_id = 1

    saved = add_veiculo(veiculo, db)

    ano = '2022'

    dados = Mock()
    dados.model_dump.return_value = {
        "modelo": "Uno Novo",
        "ano": ano
    }

    updated = update_vehicle_info(saved, dados, db)

    assert updated.modelo == "Uno Novo"
    assert updated.ano == ano

def test_delete_vehicle(db):
    veiculo = Mock()
    veiculo.modelo = "Delete"
    veiculo.marca = "Test"
    veiculo.placa = "DEL123"
    veiculo.ano = 2000
    veiculo.cliente_id = 1

    add_veiculo(veiculo, db)

    deleted = delete_vehicle("DEL123", db)

    assert deleted is not None

    result = get_vehicle("DEL123", db)
    assert result is None