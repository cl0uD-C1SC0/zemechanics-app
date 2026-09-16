from app.database import Base
from sqlalchemy import Column, Integer, String

class Usuario(Base):
    __tablename__ = "usuarios"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    senha    = Column(String(255), nullable=False)