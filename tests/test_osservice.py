import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException

from app.services.OSService import (
    criar_nova_os,
    criar_os_completa,
    consultar_os,
    avancar_os,
    aprovar_os,
    reprovar_os,
    listar_todas_os,
    atualizar_os,
    remover_os,
    adicionar_peca_os,
    remover_peca_os,
    adicionar_servico_os,
    remover_servico_os
)
from app.schemas.OrdemServicoSchema import OSCompletaSchema, VeiculoOSCompletaSchema, PecaOSCompletaSchema
from app.schemas.cliente_schema import ClienteSchema


def _dados_os_completa(pecas=None, servicos=None):
    return OSCompletaSchema(
        cliente=ClienteSchema(
            nome="Jose Silva",
            cpf="12345678901",
            endereco="Rua X, 123",
            telefone="11999999999",
            email="jose@mail.com",
        ),
        veiculo=VeiculoOSCompletaSchema(
            modelo="Civic", marca="Honda", placa="ABC1D23", ano="2020"
        ),
        pecas=pecas or [],
        servicos=servicos or [],
    )

@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.cliente_service")
def test_criar_os_sucesso(mock_cliente, mock_veiculo, mock_repo):
    db = Mock()

    os = Mock()
    os.cliente_cpf = "123"
    os.veiculo_placa = "ABC1234"

    cliente = Mock()
    cliente.cpf = "123"

    veiculo = Mock()
    veiculo.id = 1
    veiculo.placa = "ABC1234"

    mock_cliente.consultar_cliente.return_value = cliente
    mock_cliente.listar_veiculos_cliente.return_value = [veiculo]
    mock_veiculo.consultar_veiculo.return_value = veiculo

    mock_repo.validate_is_os_open.return_value = None

    nova_os = Mock()
    nova_os.id = 10
    mock_repo.create_new_os.return_value = nova_os

    result = criar_nova_os(os, db)

    assert "Nova Ordem de Serviço" in result["message"]

@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.cliente_service")
def test_criar_os_ja_existe_aberta(mock_cliente, mock_veiculo, mock_repo):
    db = Mock()

    os = Mock()
    os.cliente_cpf = "123"
    os.veiculo_placa = "ABC1234"

    cliente = Mock()
    cliente.cpf = "123"

    veiculo = Mock()
    veiculo.id = 1

    mock_cliente.consultar_cliente.return_value = cliente
    mock_cliente.listar_veiculos_cliente.return_value = [veiculo]
    mock_veiculo.consultar_veiculo.return_value = veiculo

    os_existente = Mock()
    os_existente.id = 99
    mock_repo.validate_is_os_open.return_value = os_existente

    with pytest.raises(HTTPException) as exc:
        criar_nova_os(os, db)

    assert exc.value.status_code == 409

@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.cliente_service")
def test_criar_os_veiculo_nao_pertence(mock_cliente, mock_veiculo, mock_repo):
    db = Mock()

    os = Mock()
    os.cliente_cpf = "123"
    os.veiculo_placa = "XYZ9999"

    cliente = Mock()
    cliente.cpf = "123"

    veiculo = Mock()
    veiculo.placa = "ABC1234"
    veiculo.id = 1

    mock_cliente.consultar_cliente.return_value = cliente
    mock_cliente.listar_veiculos_cliente.return_value = [veiculo]
    mock_veiculo.consultar_veiculo.return_value = veiculo

    mock_repo.validate_is_os_open.return_value = None

    with pytest.raises(HTTPException) as exc:
        criar_nova_os(os, db)

    assert exc.value.status_code == 400


@patch("app.services.OSService.PecaRepository")
def test_criar_os_completa_peca_nao_encontrada(mock_peca_repo):
    db = Mock()
    dados = _dados_os_completa(pecas=[PecaOSCompletaSchema(peca_id=1, quantidade=2)])

    mock_peca_repo.describe_peca.return_value = None

    with pytest.raises(HTTPException) as exc:
        criar_os_completa(dados, db)

    assert exc.value.status_code == 404


@patch("app.services.OSService.PecaRepository")
def test_criar_os_completa_estoque_insuficiente(mock_peca_repo):
    db = Mock()
    dados = _dados_os_completa(pecas=[PecaOSCompletaSchema(peca_id=1, quantidade=5)])

    peca = Mock()
    peca.nome = "Filtro de óleo"
    peca.quantidade = 2
    mock_peca_repo.describe_peca.return_value = peca

    with pytest.raises(HTTPException) as exc:
        criar_os_completa(dados, db)

    assert exc.value.status_code == 400


@patch("app.services.OSService.ServicosRepository")
def test_criar_os_completa_servico_nao_encontrado(mock_servico_repo):
    db = Mock()
    dados = _dados_os_completa(servicos=[1])

    mock_servico_repo.describe_service.return_value = None

    with pytest.raises(HTTPException) as exc:
        criar_os_completa(dados, db)

    assert exc.value.status_code == 404


@patch("app.services.OSService.VeiculoRepository")
@patch("app.services.OSService.cliente_repository")
@patch("app.services.OSService.cliente_service")
def test_criar_os_completa_veiculo_de_outro_cliente(mock_cliente_service, mock_cliente_repo, mock_veiculo_repo):
    db = Mock()
    dados = _dados_os_completa()

    cliente_existente = Mock()
    cliente_existente.id = 1
    mock_cliente_repo.get_specific_client.return_value = cliente_existente

    veiculo_existente = Mock()
    veiculo_existente.cliente_id = 999
    mock_veiculo_repo.get_vehicle.return_value = veiculo_existente

    with pytest.raises(HTTPException) as exc:
        criar_os_completa(dados, db)

    assert exc.value.status_code == 409


@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.VeiculoRepository")
@patch("app.services.OSService.cliente_repository")
@patch("app.services.OSService.cliente_service")
def test_criar_os_completa_veiculo_com_os_aberta(mock_cliente_service, mock_cliente_repo, mock_veiculo_repo, mock_os_repo):
    db = Mock()
    dados = _dados_os_completa()

    cliente_existente = Mock()
    cliente_existente.id = 1
    mock_cliente_repo.get_specific_client.return_value = cliente_existente

    veiculo_existente = Mock()
    veiculo_existente.id = 10
    veiculo_existente.cliente_id = 1
    mock_veiculo_repo.get_vehicle.return_value = veiculo_existente

    os_aberta = Mock()
    os_aberta.id = 77
    mock_os_repo.validate_is_os_open.return_value = os_aberta

    with pytest.raises(HTTPException) as exc:
        criar_os_completa(dados, db)

    assert exc.value.status_code == 409


@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.VeiculoRepository")
@patch("app.services.OSService.cliente_service")
@patch("app.services.OSService.cliente_repository")
def test_criar_os_completa_cliente_e_veiculo_novos(
    mock_cliente_repo, mock_cliente_service, mock_veiculo_repo, mock_veiculo_service, mock_os_repo
):
    db = Mock()
    dados = _dados_os_completa()

    mock_cliente_repo.get_specific_client.side_effect = [None, Mock(id=1, cpf=dados.cliente.cpf)]
    mock_veiculo_repo.get_vehicle.side_effect = [None, Mock(id=10, placa=dados.veiculo.placa)]

    nova_os = Mock()
    nova_os.id = 50
    mock_os_repo.create_new_os.return_value = nova_os

    result = criar_os_completa(dados, db)

    mock_cliente_service.cadastrar_cliente.assert_called_once()
    mock_veiculo_service.cadastrar_veiculo.assert_called_once()
    assert "Nova Ordem de Serviço Completa" in result["message"]
    assert "50" in result["message"]


@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.VeiculoRepository")
@patch("app.services.OSService.cliente_service")
@patch("app.services.OSService.cliente_repository")
def test_criar_os_completa_cliente_existente_atualiza(
    mock_cliente_repo, mock_cliente_service, mock_veiculo_repo, mock_veiculo_service, mock_os_repo
):
    db = Mock()
    dados = _dados_os_completa()

    cliente_existente = Mock()
    cliente_existente.id = 1
    mock_cliente_repo.get_specific_client.return_value = cliente_existente
    mock_cliente_repo.update_client_infos.return_value = cliente_existente

    mock_veiculo_repo.get_vehicle.side_effect = [None, Mock(id=10, placa=dados.veiculo.placa)]

    nova_os = Mock()
    nova_os.id = 60
    mock_os_repo.create_new_os.return_value = nova_os

    result = criar_os_completa(dados, db)

    mock_cliente_repo.update_client_infos.assert_called_once()
    mock_cliente_service.cadastrar_cliente.assert_not_called()
    assert "60" in result["message"]


@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.VeiculoRepository")
@patch("app.services.OSService.cliente_service")
@patch("app.services.OSService.cliente_repository")
def test_criar_os_completa_veiculo_existente_atualiza(
    mock_cliente_repo, mock_cliente_service, mock_veiculo_repo, mock_os_repo
):
    db = Mock()
    dados = _dados_os_completa()

    cliente_existente = Mock()
    cliente_existente.id = 1
    mock_cliente_repo.get_specific_client.return_value = cliente_existente
    mock_cliente_repo.update_client_infos.return_value = cliente_existente

    veiculo_existente = Mock()
    veiculo_existente.id = 10
    veiculo_existente.cliente_id = 1
    mock_veiculo_repo.get_vehicle.return_value = veiculo_existente
    mock_veiculo_repo.update_vehicle_info.return_value = veiculo_existente

    mock_os_repo.validate_is_os_open.return_value = None

    nova_os = Mock()
    nova_os.id = 70
    mock_os_repo.create_new_os.return_value = nova_os

    result = criar_os_completa(dados, db)

    mock_veiculo_repo.update_vehicle_info.assert_called_once()
    assert "70" in result["message"]


@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.VeiculoRepository")
@patch("app.services.OSService.cliente_service")
@patch("app.services.OSService.cliente_repository")
@patch("app.services.OSService.peca_service")
@patch("app.services.OSService.ServicosRepository")
@patch("app.services.OSService.PecaRepository")
def test_criar_os_completa_com_pecas_e_servicos(
    mock_peca_repo,
    mock_servico_repo,
    mock_peca_service,
    mock_cliente_repo,
    mock_cliente_service,
    mock_veiculo_repo,
    mock_veiculo_service,
    mock_os_repo,
):
    db = Mock()
    dados = _dados_os_completa(
        pecas=[PecaOSCompletaSchema(peca_id=1, quantidade=2)],
        servicos=[1],
    )

    peca = Mock()
    peca.id = 1
    peca.nome = "Pastilha de freio"
    peca.quantidade = 5
    mock_peca_repo.describe_peca.return_value = peca

    servico = Mock()
    servico.id = 1
    servico.nome = "Alinhamento"
    mock_servico_repo.describe_service.return_value = servico

    mock_cliente_repo.get_specific_client.side_effect = [None, Mock(id=1, cpf=dados.cliente.cpf)]
    mock_veiculo_repo.get_vehicle.side_effect = [None, Mock(id=10, placa=dados.veiculo.placa)]

    nova_os = Mock()
    nova_os.id = 80
    mock_os_repo.create_new_os.return_value = nova_os

    result = criar_os_completa(dados, db)

    mock_peca_service.remover_do_estoque.assert_called_once_with(1, 2, db)
    mock_os_repo.add_os_peca.assert_called_once_with(80, 1, 2, db)
    mock_os_repo.add_service_os.assert_called_once_with(80, 1, db)
    assert "80" in result["message"]


@patch("app.services.OSService.OSRepository")
def test_consultar_os_calculo_total(mock_repo):
    db = Mock()

    peca = Mock()
    peca.preco = 100

    servico = Mock()
    servico.preco = 50

    os_mock = Mock()
    os_mock.id = 1
    os_mock.status = "ABERTA"

    os_mock.cliente.cpf = "123"
    os_mock.veiculo.placa = "ABC"

    os_mock.pecas = [peca]
    os_mock.servicos = [servico]

    os_mock.os_pecas = [
        Mock(peca=peca, quantidade=1)
    ]

    mock_repo.get_specific_os.return_value = os_mock

    result = consultar_os(1, db)

    assert result["Total"] == 150

from app.domain.enums.StatusOS import StatusOS

@patch("app.services.OSService.OSRepository")
def test_avancar_os_sucesso(mock_repo):
    db = Mock()

    os = Mock()
    os.status = StatusOS.EM_DIAGNOSTICO

    mock_repo.get_specific_os.return_value = os
    mock_repo.advance_os.return_value = {"ok": True}

    result = avancar_os(1, db)

    assert result is not None

from app.domain.enums.StatusOS import StatusOS

@patch("app.services.OSService.OSRepository")
def test_avancar_os_bloqueado(mock_repo):
    db = Mock()

    os = Mock()
    os.status = StatusOS.AGUARDANDO_APROVACAO

    mock_repo.get_specific_os.return_value = os

    with pytest.raises(HTTPException) as exc:
        avancar_os(1, db)

    assert exc.value.status_code == 400

@patch("app.services.OSService.OSRepository")
def test_aprovar_os_sucesso(mock_repo):
    db = Mock()

    os = Mock()
    os.status = StatusOS.AGUARDANDO_APROVACAO
    os.cliente.cpf = "123"

    mock_repo.get_specific_os.return_value = os
    mock_repo.approve_os.return_value = {"ok": True}

    result = aprovar_os(1, "123", db)

    assert result is not None


@patch("app.services.OSService.OSRepository")
def test_reprovar_os_sucesso(mock_repo):
    db = Mock()

    os = Mock()
    os.status = StatusOS.AGUARDANDO_APROVACAO
    os.cliente.cpf = "123"

    mock_repo.get_specific_os.return_value = os
    mock_repo.reject_os.return_value = {"ok": True}

    result = reprovar_os(1, "123", db)

    assert result is not None
    mock_repo.reject_os.assert_called_once_with(os, db)


@patch("app.services.OSService.OSRepository")
def test_reprovar_os_nao_encontrada(mock_repo):
    db = Mock()

    mock_repo.get_specific_os.return_value = None

    with pytest.raises(HTTPException) as exc:
        reprovar_os(1, "123", db)

    assert exc.value.status_code == 404


@patch("app.services.OSService.OSRepository")
def test_reprovar_os_status_invalido(mock_repo):
    db = Mock()

    os = Mock()
    os.status = StatusOS.FINALIZADA

    mock_repo.get_specific_os.return_value = os

    with pytest.raises(HTTPException) as exc:
        reprovar_os(1, "123", db)

    assert exc.value.status_code == 400


@patch("app.services.OSService.OSRepository")
def test_reprovar_os_cpf_invalido(mock_repo):
    db = Mock()

    os = Mock()
    os.status = StatusOS.AGUARDANDO_APROVACAO
    os.cliente.cpf = "999"

    mock_repo.get_specific_os.return_value = os

    with pytest.raises(HTTPException) as exc:
        reprovar_os(1, "123", db)

    assert exc.value.status_code == 403


@patch("app.services.OSService.OSRepository")
def test_listar_os_sucesso(mock_repo):
    db = Mock()

    mock_repo.get_all_os.return_value = [1, 2]

    result = listar_todas_os(db)

    assert len(result) == 2

@patch("app.services.OSService.OSRepository")
def test_listar_os_vazio(mock_repo):
    db = Mock()

    mock_repo.get_all_os.return_value = []

    with pytest.raises(HTTPException) as exc:
        listar_todas_os(db)

    assert exc.value.status_code == 404

@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.veiculo_service")
@patch("app.services.OSService.cliente_service")
def test_atualizar_os_sucesso(mock_cliente, mock_veiculo, mock_repo):
    db = Mock()

    dados = Mock()
    dados.model_dump.return_value = {
        "veiculo_placa": "ABC123",
        "cliente_cpf": "123"
    }

    os = Mock()
    os.id = 1

    veiculo = Mock()
    veiculo.id = 10

    cliente = Mock()
    cliente.id = 20

    mock_repo.get_specific_os.return_value = os
    mock_veiculo.consultar_veiculo.return_value = veiculo
    mock_cliente.consultar_cliente.return_value = cliente

    mock_repo.update_os.return_value = os

    result = atualizar_os(1, dados, db)

    assert "atualizada com sucesso" in result["message"]

@patch("app.services.OSService.OSRepository")
def test_atualizar_os_nao_encontrada(mock_repo):
    db = Mock()

    dados = Mock()
    dados.model_dump.return_value = {}

    mock_repo.get_specific_os.return_value = None

    with pytest.raises(HTTPException):
        atualizar_os(1, dados, db)

@patch("app.services.OSService.OSRepository")
def test_remover_os_sucesso(mock_repo):
    db = Mock()

    mock_repo.get_specific_os.return_value = True
    mock_repo.remove_os.return_value = True

    result = remover_os(1, db)

    assert "sucesso" in result["message"]

@patch("app.services.OSService.OSRepository")
def test_remover_os_erro(mock_repo):
    db = Mock()

    mock_repo.get_specific_os.return_value = True
    mock_repo.remove_os.return_value = None

    with pytest.raises(HTTPException) as exc:
        remover_os(1, db)

    assert exc.value.status_code == 500

@patch("app.services.OSService.OSRepository")
def test_consultar_os_nao_encontrada(mock_repo):
    db = Mock()

    mock_repo.get_specific_os.return_value = None

    with pytest.raises(HTTPException) as exc:
        consultar_os(1, db)

    assert exc.value.status_code == 404

@patch("app.services.OSService.OSRepository")
def test_aprovar_os_status_invalido(mock_repo):
    db = Mock()

    os = Mock()
    os.status = "FINALIZADA"

    mock_repo.get_specific_os.return_value = os

    with pytest.raises(HTTPException) as exc:
        aprovar_os(1, "123", db)

    assert exc.value.status_code == 400

@patch("app.services.OSService.OSRepository")
def test_aprovar_os_cpf_invalido(mock_repo):
    db = Mock()

    os = Mock()
    os.status = "AGUARDANDO_APROVACAO"
    os.cliente.cpf = "999"

    mock_repo.get_specific_os.return_value = os

    with pytest.raises(HTTPException) as exc:
        aprovar_os(1, "123", db)

    assert exc.value.status_code == 400

@patch("app.services.OSService.PecaRepository")
@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.peca_service")
def test_adicionar_peca_os_sucesso(mock_peca_service, mock_repo, mock_peca_repo):
    db = Mock()

    os = Mock()
    peca = Mock()
    peca.quantidade = 10
    peca.nome = "Motor"

    mock_repo.get_specific_os.return_value = os
    mock_peca_repo.describe_peca.return_value = peca

    result = adicionar_peca_os(1, 1, 2, db)

    assert "adicionada" in result["message"]

@patch("app.services.OSService.OSRepository")
@patch("app.services.OSService.peca_service")
def test_remover_peca_os_sucesso(mock_peca_service, mock_repo):
    db = Mock()

    os = Mock()
    os_peca = Mock()
    os_peca.quantidade = 2

    mock_repo.get_specific_os.return_value = os
    mock_repo.get_peca_da_os.return_value = os_peca

    result = remover_peca_os(1, 1, db)

    assert "removida" in result["message"]

@patch("app.services.OSService.ServicosRepository")
@patch("app.services.OSService.OSRepository")
def test_adicionar_servico_os_sucesso(mock_repo, mock_servico_repo):
    db = Mock()

    os = Mock()
    servico = Mock()
    servico.nome = "Troca de óleo"

    mock_repo.get_specific_os.return_value = os
    mock_servico_repo.describe_service.return_value = servico

    result = adicionar_servico_os(1, 1, db)

    assert "adicionado" in result["message"]

@patch("app.services.OSService.OSRepository")
def test_remover_servico_os_sucesso(mock_repo):
    db = Mock()

    os = Mock()
    mock_repo.get_specific_os.return_value = os
    mock_repo.get_os_service.return_value = True

    result = remover_servico_os(1, 1, db)

    assert "removido" in result["message"]

from app.services.OSService import _mostrar_aprovacao

def test_mostrar_aprovacao_html():
    dados = {
        "status": "EM_ANDAMENTO",
        "veiculo_placa": "ABC123",
        "pecas": [{"nome": "Motor", "quantidade": 1, "valor": 100}],
        "servicos": [{"nome": "Troca", "valor": 50}],
        "Total": 150
    }

    response = _mostrar_aprovacao(1, dados, "123")

    assert "HTML" in str(type(response))

    corpo = response.body.decode()
    assert "OS #1 —" in corpo
    assert "Recusar OS" in corpo
    assert "/api/v1/ordem_servico/reprovar/1?cliente_cpf=123" in corpo
    assert "/api/v1/ordem_servico/confirmar_aprovacao/1?cliente_cpf=123" in corpo