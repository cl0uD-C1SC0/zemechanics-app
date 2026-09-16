from app.repositories import VeiculoRepository
from fastapi import HTTPException


def cadastrar_veiculo(veiculo, db):
    if VeiculoRepository.get_vehicle(veiculo.placa, db):
        raise HTTPException(
            status_code=409, detail="A placa solicitada já foi cadastrada no sistema"
        )

    novo_veiculo = VeiculoRepository.add_veiculo(veiculo, db)

    if not novo_veiculo:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível cadastrar o veículo, tente novamente",
        )
    return {"message": f"Veiculo cadastrado com sucesso, ID: {novo_veiculo.id}"}


def consultar_veiculo(placa, db):
    veiculo_consultado = VeiculoRepository.get_vehicle(placa, db)
    if not veiculo_consultado:
        raise HTTPException(
            status_code=404,
            detail="O Veículo com a placa solicitada não foi encontrado no sistema",
        )
    return veiculo_consultado


def atualizar_dados_veiculo(placa, dados, db):
    veiculo = VeiculoRepository.get_vehicle(placa, db)
    if not veiculo:
        raise HTTPException(
            status_code=404, detail="Veículo com essa placa não encontrado"
        )

    veiculo_atualizado = VeiculoRepository.update_vehicle_info(veiculo, dados, db)
    if not veiculo_atualizado:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível atualizar os dados do veículo, tente novamente",
        )
    return {"message": "Dados do veículo foram atualizados!"}


def listar_todos_veiculos(db):
    todos_veiculos = VeiculoRepository.get_all_vehicles(db)
    if not todos_veiculos:
        raise HTTPException(
            status_code=404, detail="Nenhum veículo foi encontrado, tente novamente"
        )
    return todos_veiculos


def remover_veiculo(veiculo_placa, db):
    if not VeiculoRepository.get_vehicle(veiculo_placa, db):
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    veiculo_deletado = VeiculoRepository.delete_vehicle(veiculo_placa, db)
    if not veiculo_deletado:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível remover o veículo, tente novamente",
        )
    return {"message": "Veículo removido com sucesso!"}
