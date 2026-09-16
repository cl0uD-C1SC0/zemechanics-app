import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services import cliente_service

@pytest.fixture
def db():
    return MagicMock()

@pytest.fixture
def cliente_mock():
    cliente = MagicMock()
    cliente.id = 1
    cliente.nome = "João Silva"
    cliente.cpf = "52998224725"
    cliente.endereco = "Rua X, 123"
    cliente.telefone = "11999999999"
    cliente.email = "joao@email.com"
    cliente.veiculos = []
    return cliente

@pytest.fixture
def veiculo_mock():
    veiculo = MagicMock()
    veiculo.id = 1
    veiculo.placa = "FGV1412"
    veiculo.modelo = "Fit"
    veiculo.marca = "Honda"
    veiculo.ano = "2014"
    return veiculo

@pytest.fixture
def cliente_schema_mock():
    schema = MagicMock()
    schema.cpf = "52998224725"
    schema.nome = "João Silva"
    schema.endereco = "Rua X, 123"
    schema.telefone = "11999999999"
    schema.email = "joao@email.com"
    return schema

class TestValidarCPF:

    def test_cpf_valido(self):
        assert cliente_service.validar_cpf("529.982.247-25") is True

    def test_cpf_valido_sem_formatacao(self):
        assert cliente_service.validar_cpf("52998224725") is True

    def test_cpf_tamanho_invalido(self):
        with pytest.raises(HTTPException) as exc:
            cliente_service.validar_cpf("123")
        assert exc.value.status_code == 400

    def test_cpf_todos_digitos_iguais(self):
        with pytest.raises(HTTPException) as exc:
            cliente_service.validar_cpf("11111111111")
        assert exc.value.status_code == 400

    def test_cpf_digito1_invalido(self):
        with pytest.raises(HTTPException) as exc:
            cliente_service.validar_cpf("52998224715")
        assert exc.value.status_code == 400

    def test_cpf_digito2_invalido(self):
        with pytest.raises(HTTPException) as exc:
            cliente_service.validar_cpf("52998224724")
        assert exc.value.status_code == 400

class TestCadastrarCliente:

    @patch("app.services.cliente_service.cliente_repository")
    def test_cadastrar_cliente_sucesso(self, mock_repo, db, cliente_mock, cliente_schema_mock):
        mock_repo.get_specific_client.return_value = None
        mock_repo.add_client.return_value = cliente_mock

        resultado = cliente_service.cadastrar_cliente(cliente_schema_mock, db)

        assert resultado["message"] == "Cliente adicionado com sucesso"
        assert resultado["cliente_id"] == str(cliente_mock.id)

    @patch("app.services.cliente_service.cliente_repository")
    def test_cadastrar_cliente_cpf_duplicado(self, mock_repo, db, cliente_mock, cliente_schema_mock):
        mock_repo.get_specific_client.return_value = cliente_mock

        with pytest.raises(HTTPException) as exc:
            cliente_service.cadastrar_cliente(cliente_schema_mock, db)
        assert exc.value.status_code == 409

    @patch("app.services.cliente_service.cliente_repository")
    def test_cadastrar_cliente_cpf_invalido(self, mock_repo, db):
        mock_repo.get_specific_client.return_value = None

        schema = MagicMock()
        schema.cpf = "00000000000"

        with pytest.raises(HTTPException) as exc:
            cliente_service.cadastrar_cliente(schema, db)
        assert exc.value.status_code == 400

class TestListarClientes:

    @patch("app.services.cliente_service.cliente_repository")
    def test_listar_clientes_sucesso(self, mock_repo, db, cliente_mock):
        mock_repo.get_all_clients.return_value = [cliente_mock]

        resultado = cliente_service.listar_clientes(db)

        assert len(resultado) == 1

    @patch("app.services.cliente_service.cliente_repository")
    def test_listar_clientes_vazio(self, mock_repo, db):
        mock_repo.get_all_clients.return_value = []

        with pytest.raises(HTTPException) as exc:
            cliente_service.listar_clientes(db)
        assert exc.value.status_code == 404


class TestListarVeiculosCliente:

    @patch("app.services.cliente_service.cliente_repository")
    def test_listar_veiculos_sucesso(self, mock_repo, db, cliente_mock, veiculo_mock):
        cliente_mock.veiculos = [veiculo_mock]
        mock_repo.get_specific_client.return_value = cliente_mock

        resultado = cliente_service.listar_veiculos_cliente(cliente_mock.cpf, db)

        assert len(resultado) == 1

    @patch("app.services.cliente_service.cliente_repository")
    def test_listar_veiculos_cliente_nao_encontrado(self, mock_repo, db):
        mock_repo.get_specific_client.return_value = None

        with pytest.raises(HTTPException) as exc:
            cliente_service.listar_veiculos_cliente("00000000000", db)
        assert exc.value.status_code == 404

    @patch("app.services.cliente_service.cliente_repository")
    def test_listar_veiculos_cliente_sem_veiculos(self, mock_repo, db, cliente_mock):
        cliente_mock.veiculos = []
        mock_repo.get_specific_client.return_value = cliente_mock

        with pytest.raises(HTTPException) as exc:
            cliente_service.listar_veiculos_cliente(cliente_mock.cpf, db)
        assert exc.value.status_code == 404


class TestRemoverCliente:

    @patch("app.services.cliente_service.cliente_repository")
    def test_remover_cliente_sucesso(self, mock_repo, db, cliente_mock):
        mock_repo.get_specific_client.return_value = cliente_mock
        mock_repo.delete_client.return_value = cliente_mock

        resultado = cliente_service.remover_cliente(cliente_mock.cpf, db)

        assert "removido com sucesso" in resultado["message"]

    @patch("app.services.cliente_service.cliente_repository")
    def test_remover_cliente_nao_encontrado(self, mock_repo, db):
        mock_repo.get_specific_client.return_value = None

        with pytest.raises(HTTPException) as exc:
            cliente_service.remover_cliente("00000000000", db)
        assert exc.value.status_code == 404

    @patch("app.services.cliente_service.cliente_repository")
    def test_remover_cliente_falha_no_banco(self, mock_repo, db, cliente_mock):
        mock_repo.get_specific_client.return_value = cliente_mock
        mock_repo.delete_client.return_value = None

        with pytest.raises(HTTPException) as exc:
            cliente_service.remover_cliente(cliente_mock.cpf, db)
        assert exc.value.status_code == 500


class TestTransferirVeiculoCliente:

    @patch("app.services.cliente_service.VeiculoRepository")
    @patch("app.services.cliente_service.cliente_repository")
    def test_transferir_veiculo_sucesso(self, mock_repo, mock_veiculo_repo, db, cliente_mock, veiculo_mock):
        mock_repo.get_specific_client.return_value = cliente_mock
        mock_veiculo_repo.get_vehicle.return_value = veiculo_mock
        mock_repo.transfer_client_vehicle.return_value = veiculo_mock

        resultado = cliente_service.transferir_veiculo_cliente(veiculo_mock.placa, cliente_mock.cpf, db)

        assert "transferido" in resultado["message"]

    @patch("app.services.cliente_service.cliente_repository")
    def test_transferir_veiculo_cliente_nao_encontrado(self, mock_repo, db, veiculo_mock):
        mock_repo.get_specific_client.return_value = None

        with pytest.raises(HTTPException) as exc:
            cliente_service.transferir_veiculo_cliente(veiculo_mock.placa, "00000000000", db)
        assert exc.value.status_code == 404

    @patch("app.services.cliente_service.VeiculoRepository")
    @patch("app.services.cliente_service.cliente_repository")
    def test_transferir_veiculo_nao_encontrado(self, mock_repo, mock_veiculo_repo, db, cliente_mock):
        mock_repo.get_specific_client.return_value = cliente_mock
        mock_veiculo_repo.get_vehicle.return_value = None

        with pytest.raises(HTTPException) as exc:
            cliente_service.transferir_veiculo_cliente("XXX0000", cliente_mock.cpf, db)
        assert exc.value.status_code == 404


class TestAtualizarInformacaoCliente:

    @patch("app.services.cliente_service.cliente_repository")
    def test_atualizar_sucesso(self, mock_repo, db, cliente_mock):
        mock_repo.get_specific_client.return_value = cliente_mock
        mock_repo.update_client_infos.return_value = cliente_mock

        dados = MagicMock()
        resultado = cliente_service.atualizar_informacao_cliente(cliente_mock.cpf, dados, db)

        assert "atualizados com sucesso" in resultado["message"]

    @patch("app.services.cliente_service.cliente_repository")
    def test_atualizar_cliente_nao_encontrado(self, mock_repo, db):
        mock_repo.get_specific_client.return_value = None

        dados = MagicMock()
        with pytest.raises(HTTPException) as exc:
            cliente_service.atualizar_informacao_cliente("00000000000", dados, db)
        assert exc.value.status_code == 404

    @patch("app.services.cliente_service.cliente_repository")
    def test_atualizar_falha_no_banco(self, mock_repo, db, cliente_mock):
        mock_repo.get_specific_client.return_value = cliente_mock
        mock_repo.update_client_infos.return_value = None

        dados = MagicMock()
        with pytest.raises(HTTPException) as exc:
            cliente_service.atualizar_informacao_cliente(cliente_mock.cpf, dados, db)
        assert exc.value.status_code == 500


class TestConsultarCliente:

    @patch("app.services.cliente_service.cliente_repository")
    def test_consultar_cliente_sucesso(self, mock_repo, db, cliente_mock):
        mock_repo.get_specific_client.return_value = cliente_mock

        resultado = cliente_service.consultar_cliente(cliente_mock.cpf, db)

        assert resultado.id == cliente_mock.id
        assert resultado.nome == cliente_mock.nome

    @patch("app.services.cliente_service.cliente_repository")
    def test_consultar_cliente_nao_encontrado(self, mock_repo, db):
        mock_repo.get_specific_client.return_value = None

        with pytest.raises(HTTPException) as exc:
            cliente_service.consultar_cliente("00000000000", db)
        assert exc.value.status_code == 404