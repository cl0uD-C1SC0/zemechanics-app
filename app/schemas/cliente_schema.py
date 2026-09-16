from pydantic import BaseModel
from typing import Optional

class ClienteSchema(BaseModel):
    nome: str
    cpf: str
    endereco: str
    telefone: str
    email: str

class ClienteUpdateSchema(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True

class ConsultAllClientsResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True

class ConsultClientResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    telefone: str
    email: str
    endereco: str
    veiculos: list["ConsultClientVeiculoResponse"] = []

    class Config:
        from_attributes = True

from app.schemas.VeiculoSchema import ConsultClientVeiculoResponse
ConsultClientResponse.model_rebuild()