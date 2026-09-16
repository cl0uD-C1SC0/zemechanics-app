from fastapi import HTTPException
from app.repositories import ServicosRepository


def adicionar_servico(servico, db):
    servico_adicionado = ServicosRepository.add_mechanic_service(servico, db)
    if not servico_adicionado:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível adicionar o serviço, tente novamente.",
        )
    return {"message": f"Serviço adicionado com sucesso, ID {servico_adicionado.id}"}


def listar_todos_servicos(db):
    servicos = ServicosRepository.get_all_services(db)
    if not servicos:
        raise HTTPException(
            status_code=404, detail="Nenhum serviço foi encontrado, tente novamente"
        )
    return servicos


def consultar_servico_especifico(servico_id, db):
    servico = ServicosRepository.describe_service(servico_id, db)
    if not servico:
        raise HTTPException(
            status_code=404,
            detail=f"Serviço com o ID: {servico_id} não foi encontrado no sistema",
        )
    return servico


def atualizar_servico_especifico(servico_id, dados, db):
    servico = ServicosRepository.describe_service(servico_id, db)

    if not servico:
        raise HTTPException(
            status_code=404,
            detail=f"Serviço com o ID: {servico_id} não foi encontrado no sistema",
        )

    servico_atualizado = ServicosRepository.update_service(servico, dados, db)
    if not servico_atualizado:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível atualizar os dados do serviço, tente novamente",
        )
    return {
        "message": f"Serviço com o ID: {servico_atualizado.id} atualizado com sucesso."
    }


def remover_servico(servico_id, db):
    servico = ServicosRepository.describe_service(servico_id, db)

    if not servico:
        raise HTTPException(
            status_code=404, detail="Serviço com esse ID não encontrado"
        )

    servico_removido = ServicosRepository.delete_service(servico_id, db)
    if not servico_removido:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível remover o serviço, tente novamente",
        )
    return {"message": "Serviço removido com sucesso"}
