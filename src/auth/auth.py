import datetime
import logging
from typing import Optional, Union

import jwt
from requests import Request


import core, error, models

__all__ = ["Key", "encode_token", "decode_token"]


def encode_token(sub, exp):
    """
    Codifica um token JWT.

    Args:
        sub (Any): O assunto do token.
        exp (Union[int, float]): O tempo de expiração do token em minutos.

    Returns:
        str: O token JWT codificado.
    """
    try:
        payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=exp),
            "iat": datetime.datetime.now(),
            "sub": sub,
        }
        result = (
            f"Bearer {jwt.encode(payload, core.settings.SECRET_KEY, algorithm='HS256')}"
        )
        return result
    except Exception as e:
        raise error.custom_HTTPException(e)


def validate_token(authorization: str) -> str:
    """
    Valida o token de autorização.

    Args:
        authorization (str): O cabeçalho de autorização contendo o token.

    Returns:
        str: O token extraído do cabeçalho de autorização.

    Raises:
        error.CustomException: Se o cabeçalho de autorização estiver ausente ou se o token estiver incorreto.
            - status_code: 401
            - detail: "Desculpe, você não tem permissão."
    """
    # Verifica se o cabeçalho de autorização está presente e contém a palavra "Bearer"
    if not authorization or "Bearer" not in authorization:
        raise error.CustomException(
            status_code=401, detail="Desculpe, você não tem permissão."
        )

    # Divide o cabeçalho de autorização para extrair o token
    token_parts = authorization.split(" ")
    # Verifica se o cabeçalho foi dividido corretamente em duas partes (tipo e token)
    if len(token_parts) != 2:
        raise error.CustomException(
            status_code=401, detail="Desculpe, você não tem permissão."
        )

    # Retorna o token extraído do cabeçalho de autorização
    return token_parts[1]


def get_user_from_payload(payload: dict) -> models.User:
    user_uuid = payload["sub"].get("user_uuid")
    if not user_uuid:
        raise error.CustomException(
            status_code=401, detail="Desculpe, você não tem permissão."
        )
    user = models.User.get("uuid", user_uuid)
    if not user:
        raise error.CustomException(
            status_code=401, detail="Desculpe, usuário não encontrado."
        )
    if not user.active:
        raise error.CustomException(
            status_code=401, detail="Desculpe, usuário desativado ou excluído."
        )
    return user


def decode_token(authorization: str, key: Union[int, None] = None) -> dict:
    try:
        token = validate_token(authorization)
        try:
            payload = jwt.decode(token, core.settings.SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            raise error.CustomException(401, "Desculpe, o token expirou.")
        except jwt.InvalidTokenError:
            raise error.CustomException(401, "Desculpe, o token é inválido.")
        if "user_uuid" in payload["sub"]:
            user = get_user_from_payload(payload)
        if key and key not in payload["sub"].get("key", []):
            raise error.CustomException(401, "Desculpe, você não tem permissão.")
        return payload["sub"]
    except Exception as e:
        raise error.custom_HTTPException(e)


class Key:
    # vefifica se o usuario tem o nivel de permissao Maximo N5
    async def n5(authorization: Optional[str]):
        payload = decode_token(authorization, 5)
        return payload

    # vefifica se o usuario tem o nivel de permissao N4
    async def n4(authorization: Optional[str]):
        payload = decode_token(authorization, 4)
        return payload

    # vefifica se o usuario tem o nivel de permissao N3
    async def n3(authorization: Optional[str]):
        payload = decode_token(authorization, 3)
        return payload

    # vefifica se o usuario tem o nivel de permissao N2
    async def n2(authorization: Optional[str]):
        payload = decode_token(authorization, 2)
        if not models.User.exist("uuid", payload["user_uuid"]):
            raise error.CustomException(
                status_code=401, detail="Usuario nao encontrado"
            )
        return payload

    # vefifica se o usuario tem o nivel de permissao minima N1
    async def n1(authorization: Optional[str]):
        payload = decode_token(authorization)
        return payload

    async def n0():
        return


# para utilizar session deve-se descomentar a liha do session midleware em mai e adicionar a lib 'itsdangerous'
class Session:
    # vefifica se o usuario tem o nivel de permissao Maximo N5
    async def n5(request: Request):
        token = request.session.get("token")
        payload = decode_token(token, 5)
        return payload

    # vefifica se o usuario tem o nivel de permissao N4
    async def n4(request: Request):
        token = request.session.get("token")
        payload = decode_token(token, 4)
        return payload

    # vefifica se o usuario tem o nivel de permissao N3
    async def n3(request: Request):
        token = request.session.get("token")
        payload = decode_token(token, 3)
        return payload

    # vefifica se o usuario tem o nivel de permissao N2
    async def n2(request: Request):
        token = request.session.get("token")
        payload = decode_token(token, 2)
        if not models.Users.get("uuid", payload["user_uuid"]):
            raise error.CustomException(
                status_code=401, detail="Usuario nao encontrado"
            )
        return payload

    # vefifica se o usuario tem o nivel de permissao minima N1
    async def n1(request: Request):
        token = request.session.get("token")
        payload = decode_token(token)
        return payload

    async def n0():
        return
