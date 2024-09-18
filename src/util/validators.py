import re
from itertools import cycle

from email_validator import EmailNotValidError, validate_email

import core, error

__all__ = [
    "validate_cpf",
    "normalize_capitalize",
    "normalize_lower",
    "normalize_password",
    "normalize_phone",
    "validate_cnpj",
    "validate_cnpj_cpf",
    "normalize_email",
    "normalize_uper",
]


def validate_cpf(cpf: str):
    if not cpf:
        return cpf
    # Remover caracteres não numéricos
    cpf = "".join(filter(str.isdigit, cpf))

    # Verificar se o CPF tem 11 dígitos
    if len(cpf) != 11:
        raise error.CustomException(
            422,
            "CPF invalido, O campo deve conter exatamente 11 digitos numericos",
        )

    # Verificar se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * len(cpf):
        raise error.CustomException(status_code=422, detail="CPF invalido")

    # Função auxiliar para calcular os dígitos verificadores
    def calcular_digito(cpf, peso):
        soma = sum(
            int(digito) * peso for digito, peso in zip(cpf, range(peso, 1, -1))
        )
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    # Validar o primeiro dígito verificador
    if cpf[9] != calcular_digito(cpf[:9], 10):
        raise error.CustomException(status_code=422, detail="CPF invalido")

    # Validar o segundo dígito verificador
    if cpf[10] != calcular_digito(cpf[:10], 11):
        raise error.CustomException(status_code=422, detail="CPF invalido")

    return cpf


# validador de CNPJ
def validate_cnpj(key: str):
    if not key:
        return key
    if len(key) != 14:
        raise error.CustomException(
            422,
            "CNPJ invalido, O campo deve conter exatamente 14 digitos numericos",
        )

    if key in (c * 14 for c in "1234567890"):
        raise error.CustomException(422, "CNPJ invalido")

    cnpj_r = key[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
    return key


# Valida um dado que pode ser CPF OU CNPJ
def validate_cnpj_cpf(key: str):
    if not key:
        return key
    if len(key) == 11:
        return validate_cpf(key)
    if len(key) == 14:
        return validate_cnpj(key)
    else:
        raise error.CustomException(422, "Deve conter um CPF ou CNPJ valido")


# Aplica Primeria letra maiuscula em uma string
def normalize_capitalize(key: str):
    if not key:
        return key
    key = key.lower()
    return " ".join((word.capitalize()) for word in key.split(" "))


def normalize_uper(key: str):
    if not key:
        return key
    return " ".join((word.upper()) for word in key.split(" "))


def normalize_password(key: bytes):
    if not key:
        return key
    return core.get_password_hash(key)


def normalize_lower(key: str):
    if not key:
        return key
    return " ".join((word.lower()) for word in key.split(" "))


def normalize_phone(key: str):
    if not key:
        return key
    key = re.sub("[^0-9]+", "", key)
    if len(key) > 13 or len(key) < 11:
        raise error.CustomException(
            status_code=422,
            detail="Formato de telefone invalido, deve conter no minimo 11 e no maximo 13 digitos",
        )
    return key


def normalize_email(key: str) -> str:
    if not key:
        return key
    try:
        try:
            valid = validate_email(key)

            key = valid.normalized
        except Exception:
            raise error.CustomException(
                status_code=422,
                detail="Formato de email invalido",
            )
    except Exception as e:
        raise error.custom_HTTPException(e)
    return key.lower()
