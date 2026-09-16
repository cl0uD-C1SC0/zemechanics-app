from app.repositories import cliente_repository
from fastapi import HTTPException
from app.repositories import VeiculoRepository


def validar_cpf(cpf):
    cpf = "".join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        raise HTTPException(status_code=400, detail="CPF Inválido")

    if cpf == cpf[0] * 11:
        raise HTTPException(status_code=400, detail="CPF Inválido")

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    digito1 = 0 if resto == 10 else resto

    if digito1 != int(cpf[9]):
        raise HTTPException(status_code=400, detail="CPF Inválido")

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    digito2 = 0 if resto == 10 else resto

    if digito2 != int(cpf[10]):
        raise HTTPException(status_code=400, detail="CPF Inválido")

    return True


def cadastrar_cliente(cliente, db):
    if cliente_repository.get_specific_client(cliente.cpf, db):
        raise HTTPException(
            status_code=409, detail="O CPF inserido já foi cadastrado no sistema"
        )

    validar_cpf(cliente.cpf)

    novo_cliente = cliente_repository.add_client(cliente, db)
    return {
        "message": "Cliente adicionado com sucesso",
        "cliente_id": f"{novo_cliente.id}",
    }


def listar_clientes(db):
    clientes = cliente_repository.get_all_clients(db)
    if not clientes:
        raise HTTPException(status_code=404, detail="Nenhum cliente cadastrado")
    return clientes


def listar_veiculos_cliente(cpf, db):
    cliente = cliente_repository.get_specific_client(cpf, db)

    if not cliente:
        raise HTTPException(
            status_code=404, detail="Cliente com esse CPF não encontrado"
        )

    if not cliente.veiculos:
        raise HTTPException(
            status_code=404, detail="Cliente não tem veículos cadastrados"
        )

    return cliente.veiculos


def remover_cliente(cpf, db):
    if not cliente_repository.get_specific_client(cpf, db):
        raise HTTPException(
            status_code=404, detail="Cliente com esse CPF não encontrado"
        )

    cliente_deletado = cliente_repository.delete_client(cpf, db)
    if cliente_deletado:
        return {
            "message": f"Cliente com o ID {cliente_deletado.id} removido com sucesso"
        }
    raise HTTPException(
        status_code=500, detail="Não foi possível remover o cliente, tente novamente"
    )


def transferir_veiculo_cliente(placa, novo_cpf, db):
    novo_cliente = cliente_repository.get_specific_client(novo_cpf, db)
    if not novo_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    veiculo = VeiculoRepository.get_vehicle(placa, db)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    veiculo_transferido = cliente_repository.transfer_client_vehicle(
        veiculo, novo_cliente, db
    )
    return {
        "message": f"Veículo com o ID: {veiculo_transferido.id} transferido para {novo_cliente.id}"
    }


def atualizar_informacao_cliente(cpf, dados, db):
    cliente = cliente_repository.get_specific_client(cpf, db)

    if not cliente:
        raise HTTPException(
            status_code=404, detail="Cliente com esse CPF não encontrado"
        )

    dados_atualizados = cliente_repository.update_client_infos(cliente, dados, db)
    if dados_atualizados:
        return {
            "message": f"Dados do cliente ID {dados_atualizados.id}, foram atualizados com sucesso"
        }
    raise HTTPException(
        status_code=500,
        detail="Não foi possível atualizar os dados do cliente, tente novamente",
    )


def consultar_cliente(cpf, db):
    cliente = cliente_repository.get_specific_client(cpf, db)
    if not cliente:
        raise HTTPException(
            status_code=404, detail="Cliente com esse CPF não encontrado"
        )

    return cliente
