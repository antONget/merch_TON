from database.models import User, Merch, Order
from database.models import async_session
import logging
from dataclasses import dataclass
from sqlalchemy import select, update


# МЕРЧ
async def get_all_merch():
    """
    Получаем всю информацию о товарах из БД
    :return:
    """
    logging.info("get_all_merch")
    async with async_session() as session:
        merch = (await session.scalars(select(Merch))).all()
        return merch


async def get_merch(id_merch: int):
    """
    Получить информацию о товаре
    :param id_merch:
    :return:
    """
    logging.info("get_merch")
    async with async_session() as session:
        merch: Merch = await session.scalar(select(Merch).where(Merch.id_merch == id_merch))
        if merch:
            return merch
        else:
            return False


async def get_merch_category(category_merch: str):
    """
    Получить информацию о товаре
    :param category_merch:
    :return:
    """
    logging.info("get_merch_category")
    async with async_session() as session:
        merch: Merch = await session.scalars(select(Merch).where(Merch.category == category_merch))
        if merch:
            return merch
        else:
            return False


# ORDER
async def add_order(data: dict):
    """
    Добавление нового заказа
    :param data:
    :return:
    """
    logging.info("add_order")
    async with async_session() as session:
        session.add(Order(**data))
        await session.commit()


async def get_all_order():
    """
    Получаем всю информацию о заказах из БД
    :return:
    """
    logging.info("get_all_merch")
    async with async_session() as session:
        orders: Order = (await session.scalars(select(Order))).all()
        return orders


async def update_address_delivery_order(id_order: int, address_delivery: str):
    """
    Обновляем адрес заказа
    :param id_order:
    :param address_delivery:
    :return:
    """
    async with async_session() as session:
        order: Order = await session.scalar(select(Order).where(Order.id_order == id_order))
        if order:
            order.address_delivery = address_delivery
            await session.commit()


async def update_size_order(id_order: int, size: str):
    """
    Обновляем адрес заказа
    :param id_order:
    :param size:
    :return:
    """
    async with async_session() as session:
        order: Order = await session.scalar(select(Order).where(Order.id_order == id_order))
        if order:
            order.size = size
            await session.commit()


async def get_order(id_order: int):
    """
    Получить информацию о заказе
    :param id_order:
    :return:
    """
    logging.info("get_user")
    async with async_session() as session:
        order: Order = await session.scalar(select(Order).where(Order.id_order == id_order))
        if order:
            return order
        else:
            return False


# USERS
async def add_user(data: dict):
    """
    Добавление нового пользователя
    :param data:
    :return:
    """
    logging.info(f"add_user: {data['id_tg']}")
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id_tg == data['id_tg']))
        if not user:
            session.add(User(**data))
            await session.commit()


async def update_name_user(id_tg: int, name: str):
    """
    Обновляем имя пользователя
    :param id_tg:
    :param name:
    :return:
    """
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id_tg == id_tg))
        if user:
            user.name = name
            await session.commit()


async def update_phone_user(id_tg: int, phone: str):
    """
    Обновляем телефон пользователя
    """
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id_tg == id_tg))
        if user:
            user.phone = phone
            await session.commit()


async def update_address_delivery_user(id_tg: int, address_delivery: str):
    """
    Обновляем адреса пользователя
    """
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id_tg == id_tg))
        if user:
            user.address_delivery = address_delivery
            await session.commit()


async def get_user(id_tg: int):
    """
    Получить информацию о пользователе
    :param id_tg:
    :return:
    """
    logging.info("get_user")
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id_tg == id_tg))
        if user:
            return user
        else:
            return False


async def update_user_data(**data):
    """
    Обновление данных о пользователе
    :param data:
    :return:
    """
    logging.info("update_user_data")
    async with async_session() as session:
        await session.execute(update(User).where(User.id_tg == data['id_tg']).values(data))
        await session.commit()


async def get_all_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users
