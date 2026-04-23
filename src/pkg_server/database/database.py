from typing import Optional
from .config import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Integer, String,
    ForeignKey
)


class PkgDatabase(Base):
    __tablename__ = "pkg"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)
    latest_version: Mapped[str] = mapped_column(String(25))

class PkgMetaData(Base):
    __tablename__ = "pkg_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pkg_id: Mapped[int] = mapped_column(Integer, ForeignKey("pkg.id"))
    version: Mapped[str] = mapped_column(String(25))
    author: Mapped[Optional[str]] = mapped_column(String(120))
    user_name: Mapped[Optional[str]] = mapped_column(String(50))
    license: Mapped[Optional[str]] = mapped_column(String(100))
