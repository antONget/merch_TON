from database.models import User, Merch, Order
from database.models import async_session


import logging
from sqlalchemy import select, update

# uncomment for testing 
# from models import User, Merch, Order
# from models import async_session




# МЕРЧ
async def get_all_merch() -> list[Merch]:
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






async def add_referral_user(main_user_id: int, referral_user_id: int):
    """
    ```
    add referral_user to "referral_users":
        main_user_id : int   (id главного пользователя)
        referral_user_id: int   (id реферала)
    ```
    """
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id == main_user_id))
        if user:
            if len(user.referral_users) != 0:
                user.referral_users += f",{referral_user_id}"
                await session.commit()
            else:
                user.referral_users += f"{referral_user_id}"
                await session.commit()


async def increase_ton_balance(tg_id: int, s: float):
    """
    ```
    increase ton_balance:
        tg_id : int
        s : float  (sum of toncoins)
    ```
    """
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id == tg_id))
        if user:
            user.ton_balance = format(user.ton_balance + s, '.4f')

            await session.commit()


""" ------------- GET METHODS -------------"""








async def _get_username_from_id(tg_id: int):
    '''```code
    returns:
        username for function "get_referral_users"
    ```'''
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id == tg_id))
        if user:
            return user.username
        else:
            return None


async def get_referral_users(tg_id: int):
    '''```python
    returns:
        По вашей реферальной ссылке подписались на бот {len(users)} пользователей:\n\n

        1. @username1
        2. @username2
        3. @username3
    ```'''
    async with async_session() as session:
        users = (await session.scalar(select(User).where(User.id == tg_id))).referral_users

        if users:
            users = users.split(",")
            s = f'По вашей реферальной ссылке подписались на бот {len(users)} пользователей:\n\n'
            c = 1
            for user_id in users:
                s += f"{c}. @{await _get_username_from_id(int(user_id))}\n"
                c += 1

            return s
        else:
            return None


async def can_add_ref_user(tg_id) -> bool:
    """
    ```
    returns:
       True if user not in db else False
    ```
    """
    async with async_session() as session:
        users = (await session.scalars(select(User))).all()
        c = 0
        for user in users:
            if user:
                if len(user.referral_users) != 0:
                    ref_users = user.referral_users.split(",")
                    for ref_user in ref_users:
                        if ref_user == str(tg_id):
                            c += 1

        if c != 0:
            return False
        return True


async def get_all_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users


async def get_user_from_id(user_id: int):
    """
    Получаем информацию из таблицы User по пользователю по его id телеграм
    """
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == user_id))
        return user


async def get_user_ton_addr_by_id(user_id: int):
    """
    Получить адрес кошелька пользователя по его id телеграм
    param: user_id - id телеграм
    """
    async with async_session() as session:
        user: User = await session.scalar(select(User).where(User.id == user_id))
        if user:
            return user.crypto_ton_addr
        else:
            return None


'''       UPDATE       '''





async def update_user_data(**data):
    '''
    Update any data in User:
        id_tg : user_tg_id 
        any datas

    '''
    async with async_session() as session:
        await session.execute(update(User).where(User.id_tg == data['id_tg']).values(data))
        await session.commit()


# import asyncio

# asyncio.run(update_user_data(**{'id_tg':1060834219, 'invoice_id':0}))
