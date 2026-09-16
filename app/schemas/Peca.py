from pydantic import BaseModel, Field
from typing import Optional
class PecaSchema(BaseModel):
    nome: str
    preco: float = Field(gt=0)
    quantidade: int

class UpdatePecaSchema(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    

class PecaResponse(BaseModel):
    id   : int
    nome : str
    preco: float
    quantidade: int

    class Config:
        from_attributes = True

class ConsultAllPecasSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True