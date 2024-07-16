from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from typing import List

engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)


async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id_tg: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(20))
    phone: Mapped[str] = mapped_column(String(15))
    address_delivery: Mapped[str] = mapped_column(String(100))
    invoice_id: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default='None')


class Merch(Base):
    __tablename__ = 'merch'

    id_merch: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(20))
    image: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Float)


class Order(Base):
    __tablename__ = 'orders'

    id_order: Mapped[int] = mapped_column(primary_key=True)
    id_tg: Mapped[int] = mapped_column(Integer)
    id_merch: Mapped[str] = mapped_column(String(20))
    count: Mapped[int] = mapped_column(Integer)
    cost: Mapped[float] = mapped_column(Float)
    address_delivery: Mapped[str] = mapped_column(String(200))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# import asyncio
#
# asyncio.run(async_main())
