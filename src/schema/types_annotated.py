from typing import Annotated

from pydantic.functional_validators import AfterValidator, BeforeValidator

import util

__all__ = [
    "Password",
    "Username",
    "Email",
    "Cpf",
    "Cnpj",
    "CpfCnpj",
]

Password = Annotated[bytes, AfterValidator(util.normalize_password)]
Username = Annotated[str, AfterValidator(util.normalize_lower)]
Email = Annotated[str, BeforeValidator(util.normalize_email)]
Cpf = Annotated[str, AfterValidator(util.validate_cpf)]
Cnpj = Annotated[str, AfterValidator(util.validate_cnpj)]
CpfCnpj = Annotated[str, AfterValidator(util.validate_cnpj_cpf)]
