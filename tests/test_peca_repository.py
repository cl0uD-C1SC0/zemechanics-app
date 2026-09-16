from unittest.mock import Mock
import pytest

from app.repositories.PecaRepository import (
    add_peca,
    get_all_pecas,
    describe_peca,
    update_peca,
    delete_peca,
    add_peca_amount,
    remove_peca_amount,
)

def test_add_peca(db):
    peca = Mock()
    peca.nome = "Filtro"
    peca.preco = 50
    peca.quantidade = 10

    result = add_peca(peca, db)

    assert result.id is not None
    assert result.nome == "Filtro"

def test_get_all_pecas(db):
    p1 = Mock()
    p1.nome = "A"
    p1.preco = 10
    p1.quantidade = 1

    p2 = Mock()
    p2.nome = "B"
    p2.preco = 20
    p2.quantidade = 2

    add_peca(p1, db)
    add_peca(p2, db)

    result = get_all_pecas(db)

    assert len(result) == 2

def test_describe_peca(db):
    peca = Mock()
    peca.nome = "Motor"
    peca.preco = 500
    peca.quantidade = 3

    saved = add_peca(peca, db)

    result = describe_peca(saved.id, db)

    assert result is not None
    assert result.nome == "Motor"

def test_update_peca(db):
    peca = Mock()
    peca.nome = "Antigo"
    peca.preco = 100
    peca.quantidade = 5

    saved = add_peca(peca, db)

    dados = Mock()
    dados.model_dump.return_value = {
        "nome": "Novo",
        "preco": 200
    }

    updated = update_peca(saved, dados, db)

    assert updated.nome == "Novo"
    assert updated.preco == 200

def test_delete_peca(db):
    peca = Mock()
    peca.nome = "Delete"
    peca.preco = 10
    peca.quantidade = 1

    saved = add_peca(peca, db)

    deleted = delete_peca(saved.id, db)

    assert deleted is not None

    result = describe_peca(saved.id, db)
    assert result is None

def test_delete_peca_inexistente(db):
    with pytest.raises(Exception):
        delete_peca(999, db)

def test_add_peca_amount(db):
    peca = Mock()
    peca.nome = "Estoque"
    peca.preco = 10
    peca.quantidade = 5

    saved = add_peca(peca, db)

    updated = add_peca_amount(saved, 3, db)

    assert updated.quantidade == 8

def test_remove_peca_amount(db):
    peca = Mock()
    peca.nome = "Estoque"
    peca.preco = 10
    peca.quantidade = 5

    saved = add_peca(peca, db)

    updated = remove_peca_amount(saved, 2, db)

    assert updated.quantidade == 3

def test_remove_peca_amount_negativo(db):
    peca = Mock()
    peca.nome = "Erro"
    peca.preco = 10
    peca.quantidade = 2

    saved = add_peca(peca, db)

    updated = remove_peca_amount(saved, 5, db)

    assert updated.quantidade < 0  # comportamento atual