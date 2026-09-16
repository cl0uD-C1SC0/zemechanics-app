from app.repositories import OSRepository
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from app.services import cliente_service as cliente_service
from app.services import peca_service as peca_service
from app.services import servico_service as servico_service
from app.services import veiculo_service as veiculo_service

from app.repositories import PecaRepository
from app.repositories import ServicosRepository
from app.repositories import cliente_repository
from app.repositories import VeiculoRepository

from app.domain.enums.StatusOS import StatusOS
from app.domain.enums.StatusOS import TRANSICAO_STATUS

from app.schemas.VeiculoSchema import VeiculoSchema, UpdateVehicleSchema
from app.schemas.cliente_schema import ClienteUpdateSchema


def criar_nova_os(os, db):

    cliente = cliente_service.consultar_cliente(os.cliente_cpf, db)
    cliente_veiculo = cliente_service.listar_veiculos_cliente(cliente.cpf, db)
    veiculo = veiculo_service.consultar_veiculo(os.veiculo_placa, db)

    os_aberta = OSRepository.validate_is_os_open(veiculo.id, db)
    if os_aberta:
        raise HTTPException(
            status_code=409,
            detail=f"Já existe uma OS aberta para este veículo — OS ID {os_aberta.id}",
        )

    placas_do_cliente = [v.placa for v in cliente_veiculo]

    if os.veiculo_placa not in placas_do_cliente:
        raise HTTPException(
            status_code=400,
            detail="O veículo inserido não pertence a este CPF"
        )

    if not cliente:
        raise HTTPException(404, detail="Cliente não encontrado!")

    if not veiculo:
        raise HTTPException(404, "Veículo não encontrado!")

    nova_os = OSRepository.create_new_os(cliente, veiculo, db)

    if nova_os:
        return {"message": f"Nova Ordem de Serviço foi criada, ID: {nova_os.id} "}


def criar_os_completa(dados, db):
    pecas_validadas = []
    for item in dados.pecas:
        peca = PecaRepository.describe_peca(item.peca_id, db)
        if not peca:
            raise HTTPException(
                status_code=404,
                detail=f"Peça com o ID {item.peca_id} não encontrada",
            )
        if peca.quantidade < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para a peça '{peca.nome}' — disponível: {peca.quantidade}",
            )
        pecas_validadas.append((peca, item.quantidade))

    servicos_validados = []
    for servico_id in dados.servicos:
        servico = ServicosRepository.describe_service(servico_id, db)
        if not servico:
            raise HTTPException(
                status_code=404,
                detail=f"Serviço com o ID {servico_id} não está cadastrado no sistema",
            )
        servicos_validados.append(servico)

    cliente_service.validar_cpf(dados.cliente.cpf)

    cliente_existente = cliente_repository.get_specific_client(dados.cliente.cpf, db)
    veiculo_existente = VeiculoRepository.get_vehicle(dados.veiculo.placa, db)

    if veiculo_existente:
        if not cliente_existente or veiculo_existente.cliente_id != cliente_existente.id:
            raise HTTPException(
                status_code=409,
                detail="Este veículo já está cadastrado para outro cliente",
            )

        os_aberta = OSRepository.validate_is_os_open(veiculo_existente.id, db)
        if os_aberta:
            raise HTTPException(
                status_code=409,
                detail=f"Já existe uma OS aberta para este veículo — OS ID {os_aberta.id}",
            )

    if cliente_existente:
        dados_atualizacao_cliente = ClienteUpdateSchema(
            nome=dados.cliente.nome,
            endereco=dados.cliente.endereco,
            telefone=dados.cliente.telefone,
            email=dados.cliente.email,
        )
        cliente = cliente_repository.update_client_infos(
            cliente_existente, dados_atualizacao_cliente, db
        )
    else:
        cliente_service.cadastrar_cliente(dados.cliente, db)
        cliente = cliente_repository.get_specific_client(dados.cliente.cpf, db)

    if veiculo_existente:
        dados_atualizacao_veiculo = UpdateVehicleSchema(
            modelo=dados.veiculo.modelo,
            marca=dados.veiculo.marca,
            ano=dados.veiculo.ano,
        )
        veiculo = VeiculoRepository.update_vehicle_info(
            veiculo_existente, dados_atualizacao_veiculo, db
        )
    else:
        veiculo_schema = VeiculoSchema(**dados.veiculo.model_dump(), cliente_id=cliente.id)
        veiculo_service.cadastrar_veiculo(veiculo_schema, db)
        veiculo = VeiculoRepository.get_vehicle(dados.veiculo.placa, db)

    nova_os = OSRepository.create_new_os(cliente, veiculo, db)

    for peca, quantidade in pecas_validadas:
        peca_service.remover_do_estoque(peca.id, quantidade, db)
        OSRepository.add_os_peca(nova_os.id, peca.id, quantidade, db)

    for servico in servicos_validados:
        OSRepository.add_service_os(nova_os.id, servico.id, db)

    return {
        "message": f"Nova Ordem de Serviço Completa foi criada com sucesso, ID: {nova_os.id}"
    }


def listar_todas_os(db):
    todas_os = OSRepository.get_all_os(db)
    if not todas_os:
        raise HTTPException(
            status_code=404, detail="Nenhuma Ordem de Serviço foi criada"
        )
    return todas_os


def atualizar_os(os_id, dados, db):
    dados_dict = dados.model_dump(exclude_none=True)

    os = OSRepository.get_specific_os(os_id, db)
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    if "veiculo_placa" in dados_dict:
        veiculo = veiculo_service.consultar_veiculo(dados_dict.pop("veiculo_placa"), db)
        if not veiculo:
            raise HTTPException(status_code=404, detail="Veículo não encontrado")
        dados_dict["veiculo_id"] = veiculo.id

    if "cliente_cpf" in dados_dict:
        cliente = cliente_service.consultar_cliente(dados_dict.pop("cliente_cpf"), db)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        dados_dict["cliente_id"] = cliente.id

    os_atualizada = OSRepository.update_os(os_id, dados_dict, db)
    return {"message": f"OS {os_atualizada.id} atualizada com sucesso"}


def remover_os(os_id, db):
    os_consultada = OSRepository.get_specific_os(os_id, db)

    if not os_consultada:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    if OSRepository.remove_os(os_id, db):
        return {"message": "OS Removida com sucesso"}
    raise HTTPException(
        status_code=500, detail="Não foi possível remover a OS, tente novamente."
    )


def consultar_os(os_id, db):
    os_consultada = OSRepository.get_specific_os(os_id, db)

    if not os_consultada:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    total_pecas = sum(p.preco for p in os_consultada.pecas)
    total_servicos = sum(s.preco for s in os_consultada.servicos)
    total = total_pecas + total_servicos

    return {
        "id": os_consultada.id,
        "status": os_consultada.status,
        "cliente_cpf": os_consultada.cliente.cpf,
        "veiculo_placa": os_consultada.veiculo.placa,
        "pecas": [
            {
                "nome": peca_add.peca.nome,
                "quantidade": peca_add.quantidade,
                "valor": peca_add.peca.preco,
            }
            for peca_add in os_consultada.os_pecas
        ],
        "servicos": [
            {"nome": service_add.nome, "valor": service_add.preco}
            for service_add in os_consultada.servicos
        ],
        "Total": round(total, 2),
    }


def avancar_os(os_id, db):
    os = OSRepository.get_specific_os(os_id, db)

    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    if os.status == StatusOS.AGUARDANDO_APROVACAO:
        raise HTTPException(
            status_code=400,
            detail="OS aguardando aprovação do cliente — use a rota /aprovar",
        )

    proximo_status = TRANSICAO_STATUS.get(os.status)

    if not proximo_status:
        raise HTTPException(status_code=400, detail="OS já está no status final")

    return OSRepository.advance_os(os, proximo_status, db)


def aprovar_os(os_id, cliente_cpf, db):
    os = OSRepository.get_specific_os(os_id, db)

    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    if os.status != StatusOS.AGUARDANDO_APROVACAO:
        raise HTTPException(status_code=400, detail="OS não está aguardando aprovação")

    if str(os.cliente.cpf) != cliente_cpf:
        raise HTTPException(status_code=403, detail="CPF não autorizado")

    return OSRepository.approve_os(os, db)


def reprovar_os(os_id, cliente_cpf, db):
    os = OSRepository.get_specific_os(os_id, db)

    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    if os.status != StatusOS.AGUARDANDO_APROVACAO:
        raise HTTPException(status_code=400, detail="OS não está aguardando aprovação")

    if str(os.cliente.cpf) != cliente_cpf:
        raise HTTPException(status_code=403, detail="CPF não autorizado")

    return OSRepository.reject_os(os, db)


def adicionar_peca_os(os_id, peca_id, quantidade, db):
    os = OSRepository.get_specific_os(os_id, db)
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    peca = PecaRepository.describe_peca(peca_id, db)
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")

    if peca.quantidade < quantidade:
        raise HTTPException(
            status_code=400,
            detail=f"Estoque insuficiente — disponível: {peca.quantidade}",
        )

    peca_service.remover_do_estoque(peca_id, quantidade, db)

    resultado = OSRepository.add_os_peca(os_id, peca_id, quantidade, db)
    return {"message": f"{quantidade}x {peca.nome} adicionada à OS {os_id}"}


def remover_peca_os(os_id, peca_id, db):
    os = OSRepository.get_specific_os(os_id, db)
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    os_peca = OSRepository.get_peca_da_os(os_id, peca_id, db)
    if not os_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada na OS")

    peca_service.adicionar_ao_estoque(peca_id, os_peca.quantidade, db)

    OSRepository.remove_os_peca(os_id, peca_id, db)
    return {"message": f"Peça removida da OS {os_id} e quantidade devolvida ao estoque"}


def adicionar_servico_os(os_id, servico_id, db):
    os = OSRepository.get_specific_os(os_id, db)
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    servico = ServicosRepository.describe_service(servico_id, db)
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    resultado = OSRepository.add_service_os(os_id, servico_id, db)
    return {"message": f"{servico.nome} adicionado à OS {os_id}"}


def remover_servico_os(os_id, servico_id, db):
    os = OSRepository.get_specific_os(os_id, db)
    if not os:
        raise HTTPException(status_code=404, detail="OS não encontrada")

    os_servico = OSRepository.get_os_service(os_id, servico_id, db)
    if not os_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado na OS")

    OSRepository.remove_service_os(os_id, servico_id, db)
    return {"message": f"Serviço removido da OS {os_id}"}


def _mostrar_aprovacao(os_id, dados_os, cliente_cpf):
    if dados_os["status"] == "Entregue":
        return {"message": "A Ordem de Serviço já foi Entregue ao Cliente."}

    if dados_os["status"] == "Finalizada":
        return {"message": "A Ordem de Serviço já foi Finalizada"}

    pecas_html = "".join(
        [
            f"<tr><td>{p['nome']}</td><td>{p['quantidade']}</td><td>R$ {p['valor']}</td></tr>"
            for p in dados_os["pecas"]
        ]
    )

    servicos_html = "".join(
        [
            f"<tr><td>{s['nome']}</td><td>R$ {s['valor']}</td></tr>"
            for s in dados_os["servicos"]
        ]
    )

    return HTMLResponse(f"""
        <html>
        <body>
            <h2>OS #{os_id} — Aguardando Aprovação</h2>
            <p><b>Status:</b> {dados_os["status"]}</p>
            <p><b>Veículo:</b> {dados_os["veiculo_placa"]}</p>

            <h3>Peças</h3>
            <table border="1">
                <tr><th>Nome</th><th>Quantidade</th><th>Valor</th></tr>
                {pecas_html}
            </table>

            <h3>Serviços</h3>
            <table border="1">
                <tr><th>Nome</th><th>Valor</th></tr>
                {servicos_html}
            </table>

            <h3>Total: R$ {dados_os["Total"]}</h3>

            <form method="post" action="/api/v1/ordem_servico/confirmar_aprovacao/{os_id}?cliente_cpf={cliente_cpf}">
                <button type="submit">✅ Aprovar OS</button>
            </form>

            <form method="post" action="/api/v1/ordem_servico/reprovar/{os_id}?cliente_cpf={cliente_cpf}">
                <button type="submit">❌ Recusar OS</button>
            </form>
        </body>
        </html>
    """)
