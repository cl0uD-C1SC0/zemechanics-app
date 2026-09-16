from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.shared_schemas import ClienteResumo
class VeiculoSchema(BaseModel):
    modelo: str
    marca: str
    placa: str
    ano: str
    cliente_id: int

class AddVehicleReponse(BaseModel):
    id: int
    cliente_id: int
    marca: str
    modelo: str
    placa: str
    ano: str
    class Config:
        from_attributes = True

class UpdateVehicleSchema(BaseModel):
    modelo: Optional[str] = None
    marca: Optional[str] = None
    ano: Optional[str] = None

class ConsultClientVeiculoResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    placa: str
    ano: str
    cliente: ClienteResumo 

    class Config:
        from_attributes = True
        populate_by_name = True

class ConsultAllVehicles(BaseModel):
    id: int
    placa: str
    class Config:
        from_attributes = True