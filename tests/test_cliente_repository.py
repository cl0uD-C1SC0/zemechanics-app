from app.repositories.cliente_repository import (
    add_client,
    get_specific_client,
    get_all_clients,
    update_client_infos,
    delete_client,
    transfer_client_vehicle,
)
from unittest.mock import Mock

def test_add_client(db):
    cliente = Mock()
    cliente.nome = "José"
    cliente.cpf = "123"
    cliente.telefone = "999"
    cliente.email = "jose@email.com"
    cliente.endereco = "Rua A"

    result = add_client(cliente, db)

    assert result.id is not None
    assert result.nome == "José"

def test_get_specific_client(db):
    cliente = Mock()
    cliente.nome = "Ana"
    cliente.cpf = "999"
    cliente.telefone = "111"
    cliente.email = "ana@email.com"
    cliente.endereco = "Rua B"

    add_client(cliente, db)

    result = get_specific_client("999", db)

    assert result is not None
    assert result.nome == "Ana"

def test_get_all_clients(db):
    c1 = Mock()
    c1.nome = "A"
    c1.cpf = "1"
    c1.telefone = "1"
    c1.email = "a@email.com"
    c1.endereco = "Rua"

    c2 = Mock()
    c2.nome = "B"
    c2.cpf = "2"
    c2.telefone = "2"
    c2.email = "b@email.com"
    c2.endereco = "Rua"

    add_client(c1, db)
    add_client(c2, db)

    result = get_all_clients(db)

    assert len(result) == 2

def test_update_client_infos(db):
    cliente = Mock()
    cliente.nome = "José"
    cliente.cpf = "123"
    cliente.telefone = "999"
    cliente.email = "jose@email.com"
    cliente.endereco = "Rua A"

    saved = add_client(cliente, db)

    dados = Mock()
    dados.model_dump.return_value = {"nome": "José Atualizado"}

    updated = update_client_infos(saved, dados, db)

    assert updated.nome == "José Atualizado"

def test_delete_client(db):
    cliente = Mock()
    cliente.nome = "Delete"
    cliente.cpf = "321"
    cliente.telefone = "000"
    cliente.email = "del@email.com"
    cliente.endereco = "Rua X"

    add_client(cliente, db)

    deleted = delete_client("321", db)

    assert deleted is not None

    result = get_specific_client("321", db)
    assert result is None

def test_transfer_client_vehicle(db):
    cliente1 = Mock()
    cliente1.nome = "A"
    cliente1.cpf = "1"
    cliente1.telefone = "1"
    cliente1.email = "a@email.com"
    cliente1.endereco = "Rua"

    cliente2 = Mock()
    cliente2.nome = "B"
    cliente2.cpf = "2"
    cliente2.telefone = "2"
    cliente2.email = "b@email.com"
    cliente2.endereco = "Rua"

    c1 = add_client(cliente1, db)
    c2 = add_client(cliente2, db)

    veiculo = Mock()
    veiculo.cliente_id = c1.id

    result = transfer_client_vehicle(veiculo, c2, db)

    assert result.cliente_id == c2.id