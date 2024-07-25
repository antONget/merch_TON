from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from config_data.config import Config, load_config
from database.requests import get_all_order, get_merch, get_user
from filter.admin_filter import check_super_admin
from datetime import datetime

import logging
import asyncio


router = Router()
user_dict = {}
config: Config = load_config()


class CreateMerch(StatesGroup):
    title_merch = State()
    photo_merch = State()
    amount_merch = State()


@router.message(F.text == '/get_order', lambda message: check_super_admin(message.chat.id))
async def process_get_order_today(message: Message, state: FSMContext) -> None:
    """
    Получить все заказы за сегодня
    """
    logging.info(f"process_create_merch {message.chat.id}")
    await state.set_state(default_state)
    all_order = await get_all_order()
    today = datetime.today().strftime('%d/%m/%Y')
    text = f'<b>Заказы выполненные {today}:</b>\n\n'
    i = 0
    for order in all_order:
        if order.date_order == today:
            i += 1
            info_merch = await get_merch(id_merch=order.id_merch)
            info_user = await get_user(id_tg=order.id_tg)
            text += f'{i}. {order.date_order} -{info_merch.title} за {info_merch.amount}TON заказал @{info_user.username} / {info_user.name}\n' \
                    f'Контактные данные: {order.address_delivery}\n\n'
        if not i % 20:
            await message.answer(text=text, parse_mode='html')
            text = ''
    if not text == '':
        await message.answer(text=text, parse_mode='html')


@router.message(F.text == '/my_referal', lambda message: check_super_admin(message.chat.id))
async def process_get_order_today(message: Message, state: FSMContext) -> None:
    """
    Получить все заказы за реферала
    """
    logging.info(f"process_create_merch {message.chat.id}")
    await state.set_state(default_state)
    # получаем все заказы
    all_order = await get_all_order()
    user = await get_user(id_tg=message.chat.id)
    text = f'<b>Заказы выполненные вашими рефералами:</b>\n\n'
    i = 0
    for order in all_order:
        if order.id_tg == user.referer_id:
            i += 1
            info_merch = await get_merch(id_merch=order.id_merch)
            info_user = await get_user(id_tg=order.id_tg)
            text += f'{i}. {order.date_order} - {info_merch.title} за {info_merch.amount}TON заказал @{info_user.username} / {info_user.name}\n'
        if not i % 20:
            await message.answer(text=text, parse_mode='html')
            text = ''
    if not text == '':
        await message.answer(text=text, parse_mode='html')