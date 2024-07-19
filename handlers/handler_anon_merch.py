from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, or_f
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from keyboards.keyboard_user import keyboards_card_merch_new
from config_data.config import Config, load_config
from database.requests import get_merch_category


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


@router.message(F.text == 'anon merch 🎱')
async def press_button_anon_category(message: Message, state: FSMContext) -> None:
    logging.info("press_button_anon_category")
    await state.set_state(default_state)
    await message.answer(text=f'20% от каждого заказа этой категории мы отправим моментально на кошелек'
                              f' казначейства проекта 🖤')
    await state.update_data(category='anon')
    await show_merch_slider(message=message, state=state)


async def show_merch_slider(message: Message, state: FSMContext):
    """
    Выводим карточки в блоках
    :param message:
    :param state:
    :return:
    """
    logging.info(f'show_merch_slider: {message.chat.id}')
    user_dict[message.chat.id] = await state.get_data()
    category = user_dict[message.chat.id]['category']
    models_merch = await get_merch_category(category_merch=category)
    list_merch = []
    for merch in models_merch:
        list_merch.append(merch)
    # выводим карточки
    keyboard = keyboards_card_merch_new(list_merch=list_merch, block=0)
    await message.answer_photo(photo=list_merch[0].image,
                               reply_markup=keyboard)


# >>
@router.callback_query(F.data.startswith('forward_'))
async def process_forward(callback: CallbackQuery, state: FSMContext):
    """
    Пагинация вперед
    :param callback: int(callback.data.split('_')[1]) номер блока для вывода
    :param state:
    :return:
    """
    logging.info(f'process_forward_game: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    category = user_dict[callback.message.chat.id]['category']
    models_merch = await get_merch_category(category_merch=category)
    list_merch = []
    for merch in models_merch:
        list_merch.append(merch)
    count_block = len(list_merch)
    num_block = int(callback.data.split('_')[1]) + 1
    if num_block == count_block:
        num_block = 0
    keyboard = keyboards_card_merch_new(list_merch=list_merch, block=num_block)
    try:
        await callback.message.edit_media(media=InputMediaPhoto(media=list_merch[num_block].image),
                                          reply_markup=keyboard)
    except:
        logging.info('ERROR')


# <<
@router.callback_query(F.data.startswith('back_'))
async def process_back(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Пагинация по списку игр игрока
    :param callback: int(callback.data.split('_')[1]) номер блока для вывода игр
    :param state:
    :return:
    """
    logging.info(f'process_back: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    category = user_dict[callback.message.chat.id]['category']
    models_merch = await get_merch_category(category_merch=category)
    list_merch = []
    for merch in models_merch:
        list_merch.append(merch)
    count_block = len(list_merch)
    num_block = int(callback.data.split('_')[1]) - 1
    if num_block < 0:
        num_block = count_block - 1
    keyboard = keyboards_card_merch_new(list_merch=list_merch, block=num_block)
    try:
        await callback.message.edit_media(media=InputMediaPhoto(media=list_merch[num_block].image),
                                          reply_markup=keyboard)
    except:
        logging.info('ERROR')
