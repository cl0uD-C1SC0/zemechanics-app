from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Servicos(Base):
    __tablename__ = "servicos"

    id          = Column(Integer, primary_key=True, index=True)
    nome        = Column(String(200), nullable=False)
    descricao   = Column(String(200), nullable=True)
    preco       = Column(Float, nullable=False)