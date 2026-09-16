from fastapi import HTTPException
from app.repositories import PecaRepository


def adicionar_peca(peca, db):
    nova_peca = PecaRepository.add_peca(peca, db)
    if not nova_peca:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível adicionar a nova peça, tente novamente",
        )
    return {"message": f"Nova peça adicionada com sucesso, ID {nova_peca.id}"}


def listar_todas_pecas(db):
    pecas = PecaRepository.get_all_pecas(db)
    if not pecas:
        raise HTTPException(
            status_code=404,
            detail="Não foi possível encontrar nenhuma peça, tente novamente",
        )
    return pecas


def consultar_peca_especifica(peca_id, db):
    peca = PecaRepository.describe_peca(peca_id, db)
    if not peca:
        raise HTTPException(
            status_code=404,
            detail=f"Peça com o ID: {peca_id} não foi encontrada no sistema",
        )
    return peca


def atualizar_peca_especifica(peca_id, dados, db):
    peca = PecaRepository.describe_peca(peca_id, db)

    if not peca:
        raise HTTPException(status_code=404, detail="Peça com esse ID não encontradoo")

    peca_atualizada = PecaRepository.update_peca(peca, dados, db)
    if not peca_atualizada:
        raise HTTPException(
            status_code=500, detail="Não foi possível atualizar a peça, tente novamente"
        )
    return {"message": f"Peça com o ID {peca_id} foi atualizada com sucesso"}


def remover_peca(peca_id, db):
    peca = PecaRepository.describe_peca(peca_id, db)
    if not peca:
        raise HTTPException(status_code=404, detail="Peça com esse ID não encontradoo")

    peca_removida = PecaRepository.delete_peca(peca_id, db)
    if not peca_removida:
        raise HTTPException(
            status_code=500, detail="Não foi possível remover a peça, tente novamente"
        )
    return {"message": "Peça removida com sucesso!"}


def adicionar_ao_estoque(peca_id, qtd_adicionar, db):
    peca = PecaRepository.describe_peca(peca_id, db)
    if not peca:
        raise HTTPException(status_code=404, detail="Peça com esse ID não encontrado")

    add_qtd = PecaRepository.add_peca_amount(peca, qtd_adicionar, db)
    if not add_qtd:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível adicionar quantidade, tente novamente",
        )
    return {
        "message": f"Adicionado {qtd_adicionar} quantidade(es) no estoque de {peca.nome}"
    }


def remover_do_estoque(peca_id, qtd_remover, db):
    peca = PecaRepository.describe_peca(peca_id, db)
    if not peca:
        raise HTTPException(status_code=404, detail="Peça com esse ID não encontrado")

    remove_qtd = PecaRepository.remove_peca_amount(peca, qtd_remover, db)
    if not remove_qtd:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível adicionar quantidade, tente novamente",
        )
    return {
        "message": f"Removido {qtd_remover} quantidade(es) do estoque de {peca.nome}"
    }
