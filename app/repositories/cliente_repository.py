from app.domain.models.cliente_model import Cliente as ClienteModel


def add_client(cliente, db):
    novo_cliente = ClienteModel(
        nome=cliente.nome,
        cpf=cliente.cpf,
        telefone=cliente.telefone,
        email=cliente.email,
        endereco=cliente.endereco,
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente


def update_client_infos(cliente, dados, db):
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)
    return cliente


def delete_client(cpf, db):
    client_to_delete = db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()

    if client_to_delete:
        db.delete(client_to_delete)
        db.commit()
        return client_to_delete


def transfer_client_vehicle(veiculo, novo_cliente, db):
    veiculo.cliente_id = novo_cliente.id
    db.commit()
    return veiculo


def get_all_clients(db):
    clientes = db.query(ClienteModel).all()
    return clientes


def get_specific_client(cpf, db):
    cliente = db.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()
    return cliente
