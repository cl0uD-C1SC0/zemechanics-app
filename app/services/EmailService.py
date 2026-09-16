import smtplib
from email.mime.text import MIMEText
import os 



def enviar_email_aprovacao(os_obj):

    SMTP_SERVER = str(os.getenv('MAIL_SERVER_ADDRESS'))

    msg = MIMEText(f"""
        Olá {os_obj.cliente.nome}!
        
        Sua os_obj #{os_obj.id} está aguardando sua aprovação.
        
        Acesse o link para aprovar:
        http://localhost:8000/api/v1/ordem_servico/aprovar/{os_obj.id}?cliente_cpf={os_obj.cliente.cpf}
        
    """)

    msg["Subject"] = f"os_obj #{os_obj.id} — Aguardando sua aprovação"
    msg["From"] = "oficina@zemechanics.com"
    msg["To"] = f"{os_obj.cliente.email}"

    try:
        with smtplib.SMTP(SMTP_SERVER, 1025) as server:
            server.sendmail(msg["From"], msg["To"], msg.as_string())

    except Exception as e:
        print(f"Erro ao enviar email: {e}")
