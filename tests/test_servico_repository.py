from unittest.mock import Mock
import pytest

from app.repositories.ServicosRepository import (
    add_mechanic_service,
    get_all_services,
    describe_service,
    update_service,
    delete_service,
)

def test_add_mechanic_service(db):
    service = Mock()
    service.nome = "Troca de óleo"
    service.preco = 150.0
    service.descricao = "Troca completa"

    result = add_mechanic_service(service, db)

    assert result.id is not None
    assert result.nome == "Troca de óleo"

def test_get_all_services(db):
    s1 = Mock()
    s1.nome = "A"
    s1.preco = 10
    s1.descricao = "desc"

    s2 = Mock()
    s2.nome = "B"
    s2.preco = 20
    s2.descricao = "desc"

    add_mechanic_service(s1, db)
    add_mechanic_service(s2, db)

    result = get_all_services(db)

    assert len(result) == 2

def test_describe_service(db):
    service = Mock()
    service.nome = "Diagnóstico"
    service.preco = 50
    service.descricao = "Check geral"

    saved = add_mechanic_service(service, db)

    result = describe_service(saved.id, db)

    assert result is not None
    assert result.nome == "Diagnóstico"

def test_update_service(db):
    service = Mock()
    service.nome = "Antigo"
    service.preco = 100
    service.descricao = "desc"

    saved = add_mechanic_service(service, db)

    dados = Mock()
    dados.model_dump.return_value = {
        "nome": "Novo",
        "preco": 200
    }

    updated = update_service(saved, dados, db)

    assert updated.nome == "Novo"
    assert updated.preco == 200

def test_delete_service(db):
    service = Mock()
    service.nome = "Delete"
    service.preco = 10
    service.descricao = "desc"

    saved = add_mechanic_service(service, db)

    deleted = delete_service(saved.id, db)

    assert deleted is not None

    result = describe_service(saved.id, db)
    assert result is None