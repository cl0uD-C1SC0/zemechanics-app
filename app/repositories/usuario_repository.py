from app.domain.models.usuario_model import Usuario

def get_usuario(username: str, db):
    return db.query(Usuario).filter(Usuario.username == username).first()

def criar_usuario(username: str, senha_hash: str, db):
    usuario = Usuario(username=username, senha=senha_hash)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def deletar_usuario(username: str, db):
    usuario = get_usuario(username, db)
    if usuario:
        db.delete(usuario)
        db.commit()
    return usuario