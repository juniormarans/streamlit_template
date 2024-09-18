import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import core, error

__all__ = ["template_string", "send_email"]


def template_string(template_name: str, content: dict) -> str:
    """Cria uma string do template a ser utilizado para envio de email.

    Args:
        template_name (str): Nome do template a ser usado.
        content (dict): Conteúdo do template.

    Returns:
        str: Retorna uma string do template preenchida com o conteúdo.
    """
    # Carrega o template do arquivo
    template_path = f"{core.settings.TEMPLATES_DIR}/{template_name}"
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()

        # Substitui as chaves no template pelos valores do dicionário 'content'
        for key, value in content.items():
            template_content = template_content.replace(f"{{{{ {key} }}}}", str(value))

        return template_content
    except FileNotFoundError:
        logging.error(f"Template {template_name} não encontrado em {core.settings.TEMPLATES_DIR}")
        raise FileNotFoundError("Template não encontrado")


def send_email(email_receiver: str, subject: str, body: str) -> None:
    """Envio de email.

    Args:
        email_receiver (str): Email do destinatário.
        subject (str): Título do Email.
        body (str): Conteúdo do email (pode ser gerado com template_string).

    Raises:
        CustomException: Caso não seja possível enviar, gera um erro.
    """
    try:
        em = MIMEMultipart()
        em.attach(MIMEText(body, "html"))
        em["From"] = core.settings.EMAILS_FROM_EMAIL
        em["Subject"] = subject
        em["To"] = email_receiver

        with smtplib.SMTP(
            "smtp.gmail.com", core.settings.SMTP_PORT, timeout=5
        ) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(
                core.settings.EMAILS_FROM_EMAIL, core.settings.SMTP_PASSWORD
            )
            smtp.sendmail(
                core.settings.EMAILS_FROM_EMAIL,
                email_receiver,
                em.as_string(),
            )
    except smtplib.SMTPException as e:
        logging.error(f"Falha ao enviar email: {e}")
        raise error.custom_HTTPException("Erro ao enviar o email")

