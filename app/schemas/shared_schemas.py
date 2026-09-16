from pydantic import BaseModel

class ClienteResumo(BaseModel):
    id: int
    nome: str
    cpf: str

    class Config:
        from_attributes = True