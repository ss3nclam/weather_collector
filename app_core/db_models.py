from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app_core.db_engine import engine


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = 'cities'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45), nullable=False)
    longitude: Mapped[str] = mapped_column(String(45), nullable=False)
    latitude: Mapped[str] = mapped_column(String(45), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"id={self.id!r}, longitude={self.longitude!r}, latitude={self.latitude!r}"


class Weather(Base):
    __tablename__ = 'weather'
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, unique=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(Integer(), ForeignKey('cities.id'), nullable=False, )
    temp: Mapped[float] = mapped_column(Float(), nullable=False)
    temp_min: Mapped[float] = mapped_column(Float(), nullable=False)
    temp_max: Mapped[float] = mapped_column(Float(), nullable=False)
    added_at = mapped_column(DateTime())

    def __repr__(self) -> str:
        return f"city_id={self.id!r}, temp={self.temp!r}, "


def create_tables():
    try:
        Base.metadata.create_all(engine)
        print('Tables were successfully created!')
    except Exception as error:
        print(f'[ERROR] - {error}')