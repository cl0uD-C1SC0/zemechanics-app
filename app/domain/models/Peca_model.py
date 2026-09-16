from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Peca(Base):
    __tablename__ = "pecas"

    id          = Column(Integer, primary_key=True, index=True)
    nome        = Column(String(100), nullable=False)
    preco       = Column(Float, nullable=False)
    quantidade  = Column(Integer, default=0)