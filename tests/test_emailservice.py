import pytest
from unittest.mock import patch, Mock
from email import message_from_string
from email.header import decode_header

from app.services.EmailService import enviar_email_aprovacao

@patch("app.services.EmailService.smtplib.SMTP")
def test_enviar_email_aprovacao_sucesso(mock_smtp):
    cliente = Mock()
    cliente.nome = "José"
    cliente.email = "jose@email.com"
    cliente.cpf = "123"

    os_obj = Mock()
    os_obj.id = 10
    os_obj.cliente = cliente

    smtp_instance = mock_smtp.return_value.__enter__.return_value

    enviar_email_aprovacao(os_obj)

    args = smtp_instance.sendmail.call_args[0]
    raw_message = args[2]

    email_msg = message_from_string(raw_message)
    subject, encoding = decode_header(email_msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    assert "os_obj #10" in subject
    assert email_msg["From"] == "oficina@zemechanics.com"
    assert email_msg["To"] == "jose@email.com"

    body = email_msg.get_payload(decode=True).decode()

    assert "José" in body
    assert "os_obj #10" in body
    assert "http://localhost:8000/api/v1/ordem_servico/aprovar/10" in body


@patch("app.services.EmailService.smtplib.SMTP")
def test_enviar_email_headers(mock_smtp):
    cliente = Mock()
    cliente.nome = "Ana"
    cliente.email = "ana@email.com"
    cliente.cpf = "999"

    os_obj = Mock()
    os_obj.id = 5
    os_obj.cliente = cliente

    smtp_instance = mock_smtp.return_value.__enter__.return_value

    enviar_email_aprovacao(os_obj)

    raw_message = smtp_instance.sendmail.call_args[0][2]

    email_msg = message_from_string(raw_message)

    subject, encoding = decode_header(email_msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    assert "os_obj #5" in subject
    assert email_msg["From"] == "oficina@zemechanics.com"
    assert email_msg["To"] == "ana@email.com"

@patch("app.services.EmailService.smtplib.SMTP")
def test_enviar_email_erro_smtp(mock_smtp):
    cliente = Mock()
    cliente.nome = "José"
    cliente.email = "jose@email.com"
    cliente.cpf = "123"

    os_obj = Mock()
    os_obj.id = 1
    os_obj.cliente = cliente

    mock_smtp.side_effect = Exception("Erro SMTP")

    enviar_email_aprovacao(os_obj)

    mock_smtp.assert_called_once()