from app.domain.models.Peca_model import Peca as PecaModel


def add_peca(peca, db):
    nova_peca = PecaModel(nome=peca.nome, preco=peca.preco, quantidade=peca.quantidade)
    db.add(nova_peca)
    db.commit()
    db.refresh(nova_peca)

    return nova_peca


def get_all_pecas(db):
    pecas = db.query(PecaModel).all()

    return pecas


def describe_peca(peca_id, db):
    peca = db.query(PecaModel).filter(PecaModel.id == peca_id).first()
    return peca


def update_peca(peca, dados, db):
    for campo, valor in dados.model_dump(exclude_none=True).items():
        setattr(peca, campo, valor)

    db.commit()
    db.refresh(peca)
    return peca


def delete_peca(peca_id, db):
    peca = db.query(PecaModel).filter(PecaModel.id == peca_id).first()

    db.delete(peca)
    db.commit()

    return peca


def add_peca_amount(peca, qtd_adicionar, db):

    peca.quantidade += qtd_adicionar
    db.commit()
    db.refresh(peca)
    return peca


def remove_peca_amount(peca, qtd_remover, db):

    peca.quantidade -= qtd_remover
    db.commit()
    db.refresh(peca)
    return peca
