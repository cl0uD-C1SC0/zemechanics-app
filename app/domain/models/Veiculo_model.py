from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Veiculo(Base):
    __tablename__ = "veiculos"

    id          = Column(Integer, primary_key=True, index=True)
    modelo      = Column(String(100), nullable=False)
    marca       = Column(String(100), nullable=False)
    placa       = Column(String(14), unique=True, nullable=False)
    ano         = Column(String(20), nullable=False)
    cliente_id  = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="veiculos")
    ordens   = relationship("OrdemDeServico", back_populates="veiculo")    