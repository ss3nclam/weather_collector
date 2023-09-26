from sqlalchemy import String, BigInteger, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app_core.db_engine import engine


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = 'wc_cities'
    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, nullable=False, unique=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(6,6), nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(6,6), nullable=False)

    def __repr__(self) -> str:
        return f"id={self.id!r}, name={self.name!r}, coordinates={self.longitude!r}, {self.latitude!r}"


def create_tables():
    Base.metadata.create_all(engine)