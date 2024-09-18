import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    CHAR,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    Text,
    column,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

import core, error, util

from .session import SessionLocal

__all__ = ["Base"]


def generate_uuid():
    return str(uuid.uuid4())


type_mapping = {
    "~": [str],
    "|": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    "<": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    ">": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    "<=": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
    ">=": [
        int,
        float,
        lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        lambda x: datetime.strptime(x, "%H:%M:%S").time(),
    ],
}


def convert_value(value, types):
    """Tenta converter um valor em uma lista de tipos especificados."""
    for conversion_fn in types:
        try:
            return conversion_fn(value)
        except Exception as e:
            last_exception = e
    raise error.CustomException(
        status_code=422,
        detail="O valor deve estar em um formato compatível com inteiros, floats, datas ou tempos.",
    )


class Response:
    def __init__(self, data: Any, meta: dict | None = None) -> None:
        self.data = data
        self.meta = meta if meta is not None else {}


class Base(DeclarativeBase):
    __name__: str
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid,
        unique=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return util.pascal_to_snake_case(cls.__name__)

    def create(self) -> object:
        try:
            _db = SessionLocal()
            data = self
            _db.add(data)
            _db.flush()
            _db.commit()
            _db.refresh(data)
            return data

        except SQLAlchemyError as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    def login(self, attribute: str, value: Any, password: str) -> object:
        """executa login em usuario

        Args:
            attribute (str): Nome do atributo para verificar o valor
            value (str): username para efetuar o login
            password (str): senha para ser verificada

        Raises:
            CustomException: 404 usuario ou senha incorretos
            CustomException: 401 status do usuario inativo
            CustomException: 401 senha incorreta_

        Returns:
            object: _description_
        """
        try:
            _db = SessionLocal()
            if not hasattr(self, attribute):
                raise error.CustomException(
                    status_code=404,
                    detail=f"Atributo '{attribute}' não encontrado na tabela '{self.__tablename__}'.",
                )

            data = (
                _db.query(self)
                .filter(getattr(self, attribute) == value)
                .first()
            )
            if not data:
                raise error.CustomException(
                    status_code=404,
                    detail="Usuario ou senha invalidos",
                )
            if hasattr(data, "active"):
                if not data.active:
                    raise error.CustomException(
                        status_code=401, detail="Usuario Inativo"
                    )

            if not core.verify_password(password, data.password):
                raise error.CustomException(
                    status_code=401,
                    detail="Usuario ou senha invalidos",
                )
            return data
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    def query_params(
        self,
        all_data: bool = False,
        attribute: str | None = None,
        value: str | None = None,
        json_string: dict | None = None,
        operator: str = "=",
        skip: int | None = None,
        limit: int | None = None,
        include: list[str] | None = None,
    ) -> object:
        """Este método realiza consultas personalizadas de acordo com a requisição do front-end.

        Args:
            all_data (bool): Se True, retorna uma lista de todos os dados equivalentes.
            attribute (str | None): Nome da chave a ser pesquisada. Deve ser um atributo válido da tabela.
            value (str | None): Conteúdo da busca relacionado à chave.
            operator (str): Operador de comparação. Padrão: "=".
            skip (int | None, optional): Número da página em caso de busca paginada.
            limit (int | None, optional): Quantidade por página.
            exclude (list[str] | None): Lista de atributos a serem excluídos da consulta.

        Raises:
            CustomException: 404 em caso de busca com um atributo não relacionado na tabela.
            CustomException: 422 em caso de uma consulta específica que não sejam passados atributos ou valores para busca.

        Returns:
            object: Retorna um objeto SQLAlchemy podendo ser vazio em caso de não encontrar nenhuma correspondência.
        """

        _db = SessionLocal()

        sub_count = False
        try:
            if include:
                for attr in include:
                    if not hasattr(self, attr):
                        raise error.CustomException(
                            status_code=404,
                            detail=f"Atributo '{attr}' não encontrado na tabela '{self.__tablename__}'.",
                        )

                atributos = [getattr(self, attr) for attr in include]
                query = select(*atributos)
            else:
                query = select(self)

            if attribute:
                # Verificar se o atributo é válido
                if not hasattr(self, attribute):
                    raise error.CustomException(
                        status_code=404,
                        detail=f"Atributo '{attribute}' não encontrado na tabela '{self.__tablename__}'.",
                    )

                # Construir a condição de filtro com base no operador
                sub_count = True
                if operator == "=":
                    query = query.filter(getattr(self, attribute) == value)
                elif operator == "~":
                    if isinstance(getattr(self, attribute).type, String):
                        query = query.filter(
                            getattr(self, attribute).ilike(
                                f"%{convert_value(value, type_mapping[operator])}%"
                            )
                        )
                    else:
                        raise error.CustomException(
                            status_code=422,
                            detail=f"o tipo do atributo a ser utilizado no operador '{operator}' deve ser String.",
                        )
                elif operator == "!":
                    query = query.filter(getattr(self, attribute) != value)
                elif operator == "<":
                    query = query.filter(
                        getattr(self, attribute)
                        < convert_value(value, type_mapping[operator])
                    )
                elif operator == ">":
                    query = query.filter(
                        getattr(self, attribute)
                        > convert_value(value, type_mapping[operator])
                    )
                elif operator == "<=":
                    query = query.filter(
                        getattr(self, attribute)
                        <= convert_value(value, type_mapping[operator])
                    )
                elif operator == ">=":
                    query = query.filter(
                        getattr(self, attribute)
                        >= convert_value(value, type_mapping[operator])
                    )
                elif operator == "|":
                    try:
                        lower, upper = value.split("|")
                        lower_value = convert_value(
                            lower, type_mapping[operator]
                        )
                        upper_value = convert_value(
                            upper, type_mapping[operator]
                        )
                        query = query.filter(
                            getattr(self, attribute).between(
                                lower_value, upper_value
                            )
                        )
                    except Exception:
                        raise error.CustomException(
                            status_code=422,
                            detail="O intervalo deve ser fornecido no formato correto, separado por '|'.",
                        )
                else:
                    raise error.CustomException(
                        status_code=422,
                        detail=f"Operador '{operator}' não é suportado.",
                    )
            if json_string:
                if not isinstance(json_string, dict):
                    raise error.CustomException(
                        status_code=422,
                        detail=f"O valor a ser utilizado deve ser um dicionário.",
                    )
                invalid_fields = [
                    field
                    for field in json_string.keys()
                    if not hasattr(self, field)
                ]
                if invalid_fields:
                    raise error.CustomException(
                        status_code=404,
                        detail=f"Os campos '{', '.join(invalid_fields)}' não encontrados na tabela '{self.__tablename__}'.",
                    )
                sub_count = True
                for field, val in json_string.items():
                    if operator == "=":
                        query = query.filter(getattr(self, field) == val)
                    elif operator == "~":
                        attribute_type = (
                            getattr(self, field).property.columns[0].type
                        )
                        if not isinstance(
                            attribute_type, (String, Text, CHAR)
                        ):
                            raise error.CustomException(
                                422,
                                f"O operador ILIKE não pode ser aplicado ao tipo de dados do atributo '{field}'.",
                            )
                        query = query.filter(
                            getattr(self, field).ilike(f"%{val}%")
                        )
                    else:
                        raise error.CustomException(
                            status_code=422,
                            detail=f"Operador '{operator}' não suportado para json_string.",
                        )

            subquery = query.subquery()
            if skip is not None and limit is not None:
                _offset = skip * limit
                query = query.offset(_offset).limit(limit)
            if all_data:
                if include:
                    data = _db.execute(query).unique().all()
                else:
                    data = _db.execute(query).unique().scalars().all()
            else:
                data = [_db.execute(query).first()]

            total_data = _db.query(func.count(self.uuid)).scalar()
            meta = {
                "total_data": total_data,
                "query_items": (
                    _db.query(func.count()).select_from(subquery)
                    if sub_count
                    else total_data
                ),
            }
            return Response(data=data, meta=meta)

        except Exception as e:
            raise error.custom_HTTPException(e)

        finally:
            _db.close()

    @classmethod
    def remove(self, uuid: UUID) -> str:
        """metodo utilizado para remover um dado da tabela correspondente

        Args:
            uuid (UUID): Id do dado a ser removido.

        Raises:
            CustomException: 404 em caso de nao encontar dado correspondete ao id remetido.
            CustomException: 400 em caso de um problema durante a exclusão

        Returns:
            str: retorna ok em caso de sucesso.
        """
        try:
            _db = SessionLocal()
            data = _db.query(self).filter_by(uuid=uuid).first()
            if not data:
                raise error.CustomException(
                    status_code=404, detail="Dado não encontrado"
                )
            _db.delete(data)
            _db.commit()
            return "OK"
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    def remove_data_and_files(self, uuid: UUID, files: list) -> str:
        """metodo utilizado para remover um dado da tabela correspondente

        Args:
            uuid (UUID): Id do dado a ser removido.

        Raises:
            CustomException: 404 em caso de nao encontar dado correspondete ao id remetido.
            CustomException: 400 em caso de um problema durante a exclusão

        Returns:
            str: retorna ok em caso de sucesso.
        """
        try:
            _db = SessionLocal()
            exclude_files = []
            data = _db.query(self).filter_by(uuid=uuid).first()
            if not data:
                raise error.CustomException(
                    status_code=404, detail="Dado não encontrado"
                )
            for f in files:
                attr = getattr(data, f)
                if attr:
                    exclude_files.append(attr)

            _db.delete(data)
            _db.commit()

            for exclude_f in exclude_files:
                util.delete_file(core.settings.UPLOAD_DIR, exclude_f)
            return "OK"
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    def flush(self) -> object:
        """Realiza um flush no banco, um processo que verifica toda a transação mas nao salva, utils para teste.

        Returns:
            object: retorna um objeto sqlalchemy
        """
        try:
            _db = SessionLocal()
            _db.add(self)
            _db.flush()
            _db.refresh(self)
            _db.close()
            return self
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    def update(self, uuid: UUID, **json_data) -> object:
        """funçao para atuilizar dados de uma tabela a partir de um dict

        Args:
            uuid (UUID): UUID do dado a ser atualizado

        Raises:
            CustomException: 404 caso nao haja correspondeica do uuid a dados nesta tabela

        Returns:
            object: retorna o objeto atualizado
        """
        try:
            _db = SessionLocal()
            data = _db.query(self).filter_by(uuid=uuid).first()
            if not data:
                raise error.CustomException(
                    status_code=404,
                    detail="Dado não encontrado",
                )
            for key, value in json_data.items():
                setattr(data, key, value)
            _db.add(data)
            _db.commit()
            _db.refresh(data)
            return data
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    async def update_form(self, uuid: UUID, files: list, **form) -> object:
        """funçao para atuilizar dados de uma tabela a partir de um dict

        Args:
            uuid (UUID): UUID do dado a ser atualizado

        Raises:
            CustomException: 404 caso nao haja correspondeica do uuid a dados nesta tabela

        Returns:
            object: retorna o objeto atualizado
        """
        try:
            _db = SessionLocal()
            list_exclude_files = []
            except_exlude_files = []
            data = _db.query(self).filter_by(uuid=uuid).first()
            if not data:
                raise error.CustomException(
                    status_code=404,
                    detail="Dado não encontrado",
                )

            for key, value in form.items():
                if value or str(type(value)) == "<class 'bool'>":
                    if key in files:
                        if getattr(data, key):
                            list_exclude_files.append(getattr(data, key))
                        filename = await util.save_file(value, "image")
                        except_exlude_files.append(filename)
                        setattr(data, key, filename)
                    else:
                        setattr(data, key, value)
            _db.add(data)
            _db.commit()
            _db.refresh(data)
            if list_exclude_files:
                for filename in list_exclude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            return data

        except Exception as e:
            if except_exlude_files:
                for filename in except_exlude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            raise error.custom_HTTPException(e)

        except:
            if except_exlude_files:
                for filename in except_exlude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            raise error.custom_HTTPException(e)

        finally:
            _db.close()

    @classmethod
    async def create_form(self, files: list, **form) -> object:
        try:
            _db = SessionLocal()
            except_exlude_files = []
            data = self()
            for key, value in form.items():
                if value:
                    for f in files:
                        if key == f:
                            filename = await util.save_file(
                                core.settings.UPLOAD_DIR, value, f[key]
                            )
                            except_exlude_files.append(filename)
                            setattr(data, key, filename)
                        else:
                            setattr(data, key, value)
            _db.add(data)
            _db.commit()
            _db.refresh(data)
            return data

        except Exception as e:
            if except_exlude_files:
                for filename in except_exlude_files:
                    util.delete_file(core.settings.UPLOAD_DIR, filename)
            raise error.custom_HTTPException(e)

        finally:
            _db.close()

    @classmethod
    def get(
        self,
        attribute: str | None = None,
        value: Any | None = None,
    ) -> object:
        """_summary_

        Args:
            attribute (str): _description_
            value (Any): _description_

        Returns:
            object: _description_
        """
        try:
            _db = SessionLocal()
            data = (
                _db.query(self)
                .filter(getattr(self, attribute) == value)
                .first()
            )

            return data
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    def count(
        cls,
        attribute: str | None = None,
        value: Any | None = None,
    ) -> int:
        """Retorna a quantidade de registros que correspondem à condição.

        Args:
            attribute (str): Nome do atributo para filtrar.
            value (Any): Valor a ser usado na condição de filtro.

        Returns:
            int: A quantidade de registros que correspondem à condição.
        """
        try:
            _db = SessionLocal()
            query = _db.query(cls)

            if attribute is not None and value is not None:
                query = query.filter(getattr(cls, attribute) == value)

            count = query.count()
            return count
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()

    @classmethod
    def unique_verify(self, attribute, value):
        try:
            _db = SessionLocal()
            data = (
                _db.query(self)
                .filter(getattr(self, attribute) == value)
                .first()
            )
            if data:
                raise error.CustomException(
                    status_code=422, detail=f"{value} ja existe"
                )
            return value
        except Exception as e:
            raise error.custom_HTTPException(e)
        finally:
            _db.close()
