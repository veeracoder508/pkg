from config import Base
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
    author: Mapped[str] = mapped_column(String(120))
    user_name: Mapped[str] = mapped_column(String(50))
    license: Mapped[str] = mapped_column(String(100))
