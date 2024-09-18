import ast
import json

class QueryParameters:
    """
    Classe para definir os parâmetros de consulta.

    Args:
        all_data (bool, optional): Indica se todas as correspondências devem ser retornadas (True)
            ou apenas a primeira correspondência (False). Default é True.
        attribute (str, optional): Nome do atributo a ser buscado. Necessário quando "value" é utilizado.
        value (str, optional): Valor do atributo a ser buscado. Necessário quando "attribute" é utilizado.
            Para especificar um intervalo, utilize "|" , onde a primeira posição representa o limite inferior
            e a segunda posição representa o limite superior do intervalo. Exemplo: "10|20" para valores entre 10 e 20.
        operator (str, optional): Operador de comparação. Utilize "=" para igualdade, "~" para busca parcial (like),
            "!" para diferente, "<" para menor que, ">" para maior que, "<=" para menor ou igual a,
            ">=" para maior ou igual a, "|" para intervalo. Default é "=".
        skip (int, optional): Número de itens a serem ignorados antes de começar a retornar os resultados. Default é 0.
        limit (int, optional): Número máximo de itens a serem retornados. Default é 100.
        include (list[str], optional): Lista de atributos a serem devolvidos na consulta, se None todos serão devolvidos.
        json_string (str, optional): Estrutura JSON com um ou mais atributos para serem pesquisados.
    """

    def __init__(
        self,
        all_data: bool = True,
        attribute: str = None,
        value: str = None,
        operator: str = "=",
        skip: int = 0,
        limit: int = 100,
        include: list = None,
        json_string: str = None,
    ):
        valid_operators = {"=", "~", "!", "<", ">", "<=", ">=", "|"}

        if operator not in valid_operators:
            raise ValueError(
                f"Operador '{operator}' inválido. Os operadores válidos são: {', '.join(valid_operators)}"
            )

        if operator == "|" and (value is None or "|" not in value):
            raise ValueError(
                "Quando o operador '|' é utilizado, o valor deve ser uma string representando o intervalo "
                "com os limites delimitados por '|'."
            )

        if (attribute is None and value is not None) or (
            attribute is not None and value is None
        ):
            raise ValueError(
                "Se um valor for fornecido, o atributo correspondente também deve ser fornecido, e vice-versa."
            )

        if not all_data and (not attribute or not value):
            raise ValueError(
                "Quando 'all_data' é False, 'attribute' e 'value' são obrigatórios!"
            )

        if skip < 0 or limit <= 0:
            raise ValueError(
                "O valor de 'skip' deve ser >= 0 e 'limit' deve ser > 0."
            )

        self.all_data = all_data
        self.attribute = attribute
        self.value = value
        self.operator = operator
        self.skip = skip
        self.limit = limit

        # Parse json_string if provided
        if json_string is not None:
            try:
                self.json_string = ast.literal_eval(json_string)
                if not isinstance(self.json_string, dict):
                    raise ValueError(
                        "O parâmetro 'json_string' deve ser uma string JSON válida representando um dicionário!"
                    )
            except (json.JSONDecodeError, ValueError):
                raise ValueError(
                    "O parâmetro 'json_string' deve ser uma string JSON válida!"
                )
        else:
            self.json_string = None

        # Validate include list if provided
        if include is not None:
            if not isinstance(include, list):
                raise ValueError(
                    "O parâmetro 'include' deve ser uma lista!"
                )
        self.include = include

    def to_dict(self):
        """
        Retorna os parâmetros como um dicionário.
        """
        return {
            "all_data": self.all_data,
            "attribute": self.attribute,
            "value": self.value,
            "operator": self.operator,
            "skip": self.skip,
            "limit": self.limit,
            "include": self.include,
            "json_string": self.json_string,
        }

