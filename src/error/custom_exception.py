import http
import logging

__all__ = ["CustomException", "custom_HTTPException"]


class ConstructException(Exception):
    """
    Classe base de exceção para construir exceções personalizadas com um código de status
    e uma mensagem de detalhe opcional.

    Atributos:
        status_code (int): O código de status HTTP associado a esta exceção.
        detail (any): A mensagem de detalhe opcional associada a esta exceção.
    """

    def __init__(self, status_code: int, detail: any = None) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail

    def __str__(self):
        return f"Status Code: {self.status_code}, Detail: {self.detail}"


class CustomException(ConstructException):
    """
    Classe de exceção personalizada que herda de ConstructException,
    permitindo a criação de exceções com um código de status e uma mensagem de detalhe.

    Atributos:
        status_code (int): O código de status HTTP associado a esta exceção.
        detail (any): A mensagem de detalhe opcional associada a esta exceção.
    """

    def __init__(self, status_code: int, detail: any = None):
        super().__init__(status_code, detail)


def custom_HTTPException(e: any) -> None:
    """
    Função para manipular exceções personalizadas, logar um aviso se a exceção
    não tiver um código de status, e lançar uma exceção com um código de status
    e uma mensagem de detalhe.

    Args:
        e (any): A exceção a ser manipulada.

    Raises:
        CustomException: Uma exceção personalizada com um código de status
                         e uma mensagem de detalhe.
    """
    if not hasattr(e, "status_code"):
        logging.warning("Exceção sem código de status foi capturada.")
        raise CustomException(status_code=555, detail="Erro Interno API")
    raise CustomException(status_code=e.status_code, detail=e.detail)


