from pydantic import BaseModel, Field
from typing import Optional

class ServicoSchema(BaseModel):
    nome: str
    preco: float = Field(gt=0)
    descricao: str
class UpdateServiceSchema(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    descricao: Optional[str] = None

class ServicoResponse(BaseModel):
    id   : int
    nome : str
    preco: float
    class Config:
        from_attributes = True

class ConsultAllServicosSchema(BaseModel):
    id: int
    nome: str