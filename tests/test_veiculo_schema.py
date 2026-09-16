import pytest
from pydantic import ValidationError

from app.schemas.VeiculoSchema import (
    VeiculoSchema,
    AddVehicleReponse,
    UpdateVehicleSchema,
    ConsultClientVeiculoResponse,
    ConsultAllVehicles,
)

def test_veiculo_schema_valido():
    data = {
        "modelo": "Civic",
        "marca": "Honda",
        "placa": "ABC1234",
        "ano": "2020",
        "cliente_id": 1
    }

    veiculo = VeiculoSchema(**data)

    assert veiculo.modelo == "Civic"
    assert veiculo.cliente_id == 1

def test_veiculo_schema_invalido():
    data = {
        "modelo": "Civic"
        # faltando campos obrigatórios
    }

    with pytest.raises(ValidationError):
        VeiculoSchema(**data)

def test_add_vehicle_response_valido():
    data = {
        "id": 1,
        "cliente_id": 1,
        "marca": "Honda",
        "modelo": "Civic",
        "placa": "ABC1234",
        "ano": "2020"
    }

    result = AddVehicleReponse.model_validate(data)

    assert result.id == 1
    assert result.placa == "ABC1234"

def test_update_vehicle_schema_parcial():
    data = {
        "marca": "Toyota"
    }

    veiculo = UpdateVehicleSchema(**data)

    assert veiculo.marca == "Toyota"
    assert veiculo.modelo is None

def test_update_vehicle_schema_dump():
    data = {
        "modelo": "Corolla",
        "marca": None
    }

    veiculo = UpdateVehicleSchema(**data)

    result = veiculo.model_dump(exclude_none=True)

    assert "modelo" in result
    assert "marca" not in result

def test_consult_client_veiculo_response():
    data = {
        "id": 1,
        "marca": "Honda",
        "modelo": "Civic",
        "placa": "ABC1234",
        "ano": "2020",
        "cliente": {
            "id": 1,
            "nome": "José",
            "cpf": "123"
        }
    }

    result = ConsultClientVeiculoResponse.model_validate(data)

    assert result.cliente.nome == "José"
    assert result.modelo == "Civic"

def test_consult_client_veiculo_response_invalido():
    data = {
        "id": 1,
        "marca": "Honda",
        # faltando campos
    }

    with pytest.raises(ValidationError):
        ConsultClientVeiculoResponse.model_validate(data)

def test_consult_all_vehicles():
    data = {
        "id": 1,
        "placa": "ABC1234"
    }

    result = ConsultAllVehicles.model_validate(data)

    assert result.id == 1
    assert result.placa == "ABC1234"