from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.cliente_schema import ClienteSchema

class OrdemDeServicoSchema(BaseModel):
    cliente_cpf: int
    veiculo_placa: str

class OSUpdateSchema(BaseModel):
    cliente_cpf: Optional[int] = None
    veiculo_placa: Optional[str] = None

class ClienteResumo(BaseModel):
    id: int
    nome: str
    cpf: str
    class Config:
        from_attributes = True
class VeiculoResumo(BaseModel):
    id: int
    marca: str
    modelo: str
    placa: str
    
    class Config:
        from_attributes = True
class OSResponse(BaseModel):
    id: int
    status: str
    criado_em: datetime
    cliente: ClienteResumo
    veiculo: VeiculoResumo

    class Config:
        from_attributes = True

class VeiculoOSCompletaSchema(BaseModel):
    modelo: str
    marca: str
    placa: str
    ano: str

class PecaOSCompletaSchema(BaseModel):
    peca_id: int
    quantidade: int = Field(gt=0)

class OSCompletaSchema(BaseModel):
    cliente: ClienteSchema
    veiculo: VeiculoOSCompletaSchema
    pecas: list[PecaOSCompletaSchema] = []
    servicos: list[int] = []