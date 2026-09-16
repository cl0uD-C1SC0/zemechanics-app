from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from app.api.router import router
from app.database import Base, engine
# from app.core.security import verificar_token # > TRANSFERIDO PARA FUNÇÃO LAMBDA
from app.core.init_db import init_db

from app.domain.models.cliente_model import Cliente
from app.domain.models.Veiculo_model import Veiculo
from app.domain.models.Peca_model import Peca
from app.domain.models.Servico_model import Servicos
from app.domain.models.OrdemServico_model import OrdemDeServico, OSPeca, OSServico
from app.domain.models.usuario_model import Usuario

Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="Ze Mechanics LTDA",
    description="Swagger UI - FIAP",
    version="1.0",
    docs_url=None,
    contact={"RM": "rm371895", "Nome": "Jose Silva"},
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# TRANSFERIDO PARA FUNÇÃO LAMBDA
# CADASTRAR AS ROTAS PUBLICAS ABAIXO NO AWS API GATEWAY
# ROTAS_PUBLICAS = [
#     "/api/v1/auth/login",
#     "/api/v1/auth/registrar",
#     "/api/v1/ordem_servico/aprovar",
#     "/api/v1/ordem_servico/confirmar_aprovacao",
#     "/api/v1/ordem_servico/reprovar",
#     "/api/v1/health",
#     "/docs",
#     "/openapi.json",
#     "/static",
# ]

# TRANSFERIDO PARA FUNÇÃO LAMBDA
# @app.middleware("http")
# async def jwt_middleware(request: Request, call_next):
#     for rota in ROTAS_PUBLICAS:
#         if request.url.path.startswith(rota):
#             return await call_next(request)

#     token = request.headers.get("Authorization")
#     if not token or not token.startswith("Bearer "):
#         return JSONResponse(status_code=401, content={"detail": "Token não fornecido"})

#     payload = verificar_token(token.split(" ")[1])
#     if not payload:
#         return JSONResponse(status_code=401, content={"detail": "Token inválido ou expirado"})

#     return await call_next(request)

@app.get("/docs", include_in_schema=False)
async def custom_swagger():
    return get_swagger_ui_html(
        openapi_url="openapi.json",
        title="Ze Mechanics LTDA",
        swagger_favicon_url="static/images/Logo-ZeMechanicsLTDA.ico",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "agate",
            "docExpansion": "none",
            "filter": True,
            "displayRequestDuration": True
            # "persistAuthorization": True,
        },
    )

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
#     schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }
#     schema["security"] = [{"BearerAuth": []}]
#     app.openapi_schema = schema
#     return schema

# app.openapi = custom_openapi

app.include_router(router, prefix="/api/v1")