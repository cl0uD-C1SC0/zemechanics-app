import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

from app.domain.models.Cliente_model import Cliente
from app.domain.models.Veiculo_model import Veiculo
from app.domain.models.Peca_model import Peca
from app.domain.models.Servico_model import Servicos
from app.domain.models.OrdemServico_model import OrdemDeServico, OSPeca, OSServico
from app.domain.models.usuario_model import Usuario

# ── BANCO DE DADOS DE TESTE (SQLite em memória) ────────────────────────────────
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ── FIXTURE PRINCIPAL COM JWT ──────────────────────────────────────────────────
@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        # Registra usuário de teste
        c.post(
            "/api/v1/auth/registrar",
            data={"username": "admin_test", "password": "admin123"},
        )

        # Loga e pega o token
        response = c.post(
            "/api/v1/auth/login",
            data={"username": "admin_test", "password": "admin123"},
        )

        assert response.status_code == 200, "Falha no login — verifique a rota /auth/login"
        token = response.json()["access_token"]

        # Injeta o token em TODAS as requisições automaticamente
        c.headers.update({"Authorization": f"Bearer {token}"})

        yield c

    Base.metadata.drop_all(bind=engine)


# ── DADOS DO TESTE ─────────────────────────────────────────────────────────────
CLIENTE_DATA = {
    "nome": "João Silva",
    "cpf": "52998224725",
    "endereco": "Rua X, 123",
    "telefone": "11999999999",
    "email": "joao@zemechanics.com",
}

VEICULO_DATA = {
    "modelo": "Fit",
    "marca": "Honda",
    "placa": "FGV1412",
    "ano": "2014",
    "cliente_id": None,  # preenchido dinamicamente
}

PECA_DATA = {
    "nome": "Filtro de Óleo",
    "preco": 45.90,
    "quantidade": 20,
}

SERVICO_DATA = {
    "nome": "Troca de Óleo",
    "preco": 120.00,
    "descricao": "Troca completa de óleo do motor",
}


# ── TESTE DE INTEGRAÇÃO: FLUXO PRINCIPAL ──────────────────────────────────────
class TestFluxoPrincipal:

    cliente_id = None
    veiculo_id = None
    peca_id    = None
    servico_id = None
    os_id      = None

    def test_01_cadastrar_cliente(self, client):
        response = client.post("/api/v1/cliente/novo_cliente", json=CLIENTE_DATA)

        assert response.status_code == 201
        assert "cliente_id" in response.json()

        TestFluxoPrincipal.cliente_id = int(response.json()["cliente_id"])

    def test_02_cadastrar_veiculo(self, client):
        veiculo = {**VEICULO_DATA, "cliente_id": self.cliente_id}
        response = client.post("/api/v1/veiculo/cadastrar_veiculo", json=veiculo)

        assert response.status_code == 201
        assert "Veiculo cadastrado com sucesso" in response.json()["message"]

        veiculo_id = int(response.json()["message"].split("ID: ")[-1])
        TestFluxoPrincipal.veiculo_id = veiculo_id

    def test_03_cadastrar_peca(self, client):
        response = client.post("/api/v1/peca/adicionar_peca", json=PECA_DATA)

        assert response.status_code == 201
        assert "Nova peça adicionada com sucesso" in response.json()["message"]

        TestFluxoPrincipal.peca_id = int(response.json()["message"].split("ID ")[-1])

    def test_04_cadastrar_servico(self, client):
        response = client.post("/api/v1/servico/adicionar_servico", json=SERVICO_DATA)

        assert response.status_code == 201
        assert "Serviço adicionado com sucesso" in response.json()["message"]

        TestFluxoPrincipal.servico_id = int(response.json()["message"].split("ID ")[-1])

    def test_05_criar_os(self, client):
        response = client.post(
            "/api/v1/ordem_servico/nova_os",
            json={
                "cliente_cpf": int(CLIENTE_DATA["cpf"]),
                "veiculo_placa": VEICULO_DATA["placa"],
            },
        )

        assert response.status_code == 201
        assert "Nova Ordem de Serviço foi criada" in response.json()["message"]

        os_id = response.json()["message"].split("ID: ")[-1]
        TestFluxoPrincipal.os_id = os_id

    def test_06_adicionar_peca_na_os(self, client):
        response = client.post(
            f"/api/v1/ordem_servico/{self.os_id}/adicionar_peca/{self.peca_id}?quantidade=2"
        )

        assert response.status_code == 200
        assert "message" in response.json()

    def test_07_adicionar_servico_na_os(self, client):
        response = client.post(
            f"/api/v1/ordem_servico/{self.os_id}/adicionar_servico/{self.servico_id}"
        )

        assert response.status_code == 200
        assert "message" in response.json()

    def test_08_avancar_os_para_em_diagnostico(self, client):
        response = client.patch(f"/api/v1/ordem_servico/avancar/{self.os_id}")

        assert response.status_code == 200
        assert "Em Diagnóstico" in response.json()["message"]

    def test_09_avancar_os_para_aguardando_aprovacao(self, client):
        response = client.patch(f"/api/v1/ordem_servico/avancar/{self.os_id}")

        assert response.status_code == 200
        assert "Aguardando Aprovação" in response.json()["message"]

    def test_10_aprovar_os(self, client):
        with TestClient(app) as public_client:  # client sem token
            response = public_client.post(
                f"/api/v1/ordem_servico/confirmar_aprovacao/{self.os_id}?cliente_cpf={CLIENTE_DATA['cpf']}"
            )

        assert response.status_code == 200
        assert "message" in response.json()

    def test_11_avancar_os_para_finalizada(self, client):
        response = client.patch(f"/api/v1/ordem_servico/avancar/{self.os_id}")

        assert response.status_code == 200
        assert "Finalizada" in response.json()["message"]

    def test_12_avancar_os_para_entregue(self, client):
        response = client.patch(f"/api/v1/ordem_servico/avancar/{self.os_id}")

        assert response.status_code == 200
        assert "Entregue" in response.json()["message"]

    def test_13_consultar_os_entregue(self, client):
        response = client.get(f"/api/v1/ordem_servico/consultar/{self.os_id}")

        assert response.status_code == 200
        dados = response.json()
        assert dados["status"] == "Entregue"
        assert len(dados["pecas"]) > 0
        assert len(dados["servicos"]) > 0
        assert dados["Total"] > 0