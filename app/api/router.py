from fastapi import APIRouter
from app.api.v1 import cliente_api, ordemservico_api, peca_api, servico_api, veiculo_api, auth_router, health_api


router = APIRouter()

router.include_router(cliente_api.router)
router.include_router(veiculo_api.router)
router.include_router(ordemservico_api.router)
router.include_router(peca_api.router)
router.include_router(servico_api.router)
#router.include_router(auth_router.router)
router.include_router(health_api.router)