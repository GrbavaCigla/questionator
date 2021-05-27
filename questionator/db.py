from typing import Any
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from .config import settings

if os.environ.get("DATABASE_URL"):
    engine = create_engine(os.environ.get("DATABASE_URL"), pool_pre_ping=True)
else:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id: Any
