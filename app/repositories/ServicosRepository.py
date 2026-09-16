from app.domain.models.Servico_model import Servicos as ServicoModel


def add_mechanic_service(service, db):
    novo_servico = ServicoModel(
        nome=service.nome, preco=service.preco, descricao=service.descricao
    )
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico


def get_all_services(db):
    servicos = db.query(ServicoModel).all()
    return servicos


def describe_service(servico_id, db):
    servico = db.query(ServicoModel).filter(ServicoModel.id == servico_id).first()
    return servico


def update_service(servico, dados, db):
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(servico, campo, valor)

    db.commit()
    db.refresh(servico)
    return servico


def delete_service(servico_id, db):
    servico = db.query(ServicoModel).filter(ServicoModel.id == servico_id).first()

    db.delete(servico)
    db.commit()

    return servico
