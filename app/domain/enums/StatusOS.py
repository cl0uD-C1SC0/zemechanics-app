from enum import Enum

class StatusOS(str, Enum):
    RECEBIDA                = "Recebida"
    EM_DIAGNOSTICO          = "Em Diagnóstico"
    AGUARDANDO_APROVACAO    = "Aguardando Aprovação"
    REPROVADA               = "Reprovada"
    EM_EXECUCAO             = "Em Execução"
    FINALIZADA              = "Finalizada"
    ENTREGUE                = "Entregue"

TRANSICAO_STATUS = {
    StatusOS.RECEBIDA        : StatusOS.EM_DIAGNOSTICO,
    StatusOS.EM_DIAGNOSTICO  : StatusOS.AGUARDANDO_APROVACAO,
    StatusOS.EM_EXECUCAO     : StatusOS.FINALIZADA,
    StatusOS.FINALIZADA      : StatusOS.ENTREGUE,
}