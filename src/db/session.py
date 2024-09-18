import logging
from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import core

__all__ = ["SessionLocal", "engine"]

# Configurando o log para exibir as queries
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine(
    core.settings.SQLALCHEMY_DATABASE_URI, pool_size=20, max_overflow=0
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
