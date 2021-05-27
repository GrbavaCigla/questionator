from typing import Any
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

if os.environ.get("DATABASE_URL"):
    # Heroku
    uri = os.environ.get("DATABASE_URL")
    uri = "postgresql" + uri[9:] 
    engine = create_engine(uri, pool_pre_ping=True)
else:
    from .config import settings
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    id: Any
