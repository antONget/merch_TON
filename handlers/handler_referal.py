from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, LinkPreviewOptions
# from aiogram.filters import CommandStart, or_f
# from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.utils.deep_linking import create_start_link, decode_payload
from keyboards.keyboard_referal import keyboard_refer
from config_data.config import Config, load_config
# from database.requests import get_merch, get_all_order, add_order, add_user, update_name_user,\
#     update_phone_user, update_address_delivery_user, update_address_delivery_order, get_user, get_order,\
#     get_merch_category, update_user_data, update_size_order
# from datetime import datetime
# from cryptoh.CryptoHelper import XRocketPayStatus, XRocketPayCurrency, x_roket_pay


import logging
import asyncio


router = Router()
user_dict = {}
config: Config = load_config()


class Merch(StatesGroup):
    username = State()
    phone = State()
    address_delivery = State()
    count_merch = State()
    id_merch = State()
    custom = State()


@router.message(F.text == 'referral program 💵🥂')
async def press_button_refer(message: Message, state: FSMContext) -> None:
    """
    Получение реф ссылки
    """
    logging.info("press_button_refer")
    await state.set_state(default_state)
    await message.answer(text=f'Размести торговую карточку в своем комьюнити/группе и получай комиссию 20% с каждой'
                              f' покупки моментально на свой кошелек 😉',
                         reply_markup=keyboard_refer())


@router.callback_query(F.data.startswith('refer'))
async def process_refer(callback: CallbackQuery, bot: Bot):
    logging.info(f'process_refer: {callback.message.chat.id}')
    link = await create_start_link(bot=bot, payload=str(callback.message.chat.id), encode=True)
    await callback.message.answer(text=f'Ваша реферальная ссылка:\n'
                                       f'{link}\n\n'
                                       f'Используйте ее чтобы добавить на ваш ресурс и получать 20% за приобретенные'
                                       f' продукты с вашей рекламы',
                                  link_preview_options=LinkPreviewOptions(is_disabled=True))
