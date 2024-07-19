from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from config_data.config import Config, load_config
from database.requests import get_all_merch, add_merch
from keyboards.keyboards_add_merch import keyboard_add_merch, keyboard_add_merch_anon
from filter.admin_filter import check_super_admin


import logging
import asyncio


router = Router()
user_dict = {}
config: Config = load_config()


class CreateMerch(StatesGroup):
    title_merch = State()
    photo_merch = State()
    amount_merch = State()


@router.message(F.text == '/add_merch', lambda message: check_super_admin(message.chat.id))
async def process_create_merch(message: Message, state: FSMContext) -> None:
    """
    Начало диалога создания merch
    """
    logging.info(f"process_create_merch {message.chat.id}")
    await state.set_state(default_state)
    await message.answer(text='Выберите категорию создаваемого merch',
                         reply_markup=keyboard_add_merch())


@router.callback_query(F.data.startswith('add_merch_'))
@router.callback_query(F.data.startswith('anonadd_merch_'))
async def process_create_title_merch(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Добавление названия merch
    """
    logging.info(f"process_create_title_merch {callback.message.chat.id}")
    create_category = callback.data.split('_')[2]
    await state.update_data(create_category=create_category)
    if create_category == 'anon':
        await callback.message.answer(text='Выберите категорию создаваемого merch',
                                      reply_markup=keyboard_add_merch_anon())
        return
    await state.update_data(create_product=create_category)
    await callback.message.edit_text(text='Пришлите название merch, для его идентификации.'
                                          ' Например: Кружка черная (blue TON)',
                                     reply_markup=None)
    await state.set_state(CreateMerch.title_merch)


@router.message(F.text, StateFilter(CreateMerch.title_merch))
async def process_create_photo_merch(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем название merch и запрашиваем его фото
    """
    logging.info(f"process_create_photo_merch {message.chat.id}")
    create_title = message.text
    await state.update_data(create_title=create_title)
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text='Пришлите стоимость merch')
    await state.set_state(CreateMerch.amount_merch)


@router.message(F.text, StateFilter(CreateMerch.amount_merch), lambda message: message.text.isdigit())
async def process_create_amount_merch(message: Message, state: FSMContext) -> None:
    """
    Получаем стоимость merch и запрашиваем его фото
    """
    logging.info(f"process_create_amount_merch {message.chat.id}")
    create_amount = int(message.text)
    await state.update_data(create_amount=create_amount)
    await message.answer('Пришлите изображение merch')
    await state.set_state(CreateMerch.photo_merch)


@router.message(F.text, StateFilter(CreateMerch.amount_merch))
async def process_create_amount_merch_error(message: Message, state: FSMContext) -> None:
    """
    Получаем стоимость merch и запрашиваем его фото
    """
    logging.info(f"process_create_amount_merch_error {message.chat.id}")
    await message.answer('Некорректно. Пришлите число')
    await state.set_state(CreateMerch.amount_merch)


@router.message(F.photo, StateFilter(CreateMerch.photo_merch))
async def process_add_merch(message: Message, state: FSMContext) -> None:
    """
    Получаем изображение merch
    :param message:
    :param state:
    :return:
    """
    logging.info('process_add_merch')
    photo = message.photo[-1].file_id
    user_dict[message.chat.id] = await state.get_data()
    id_merch = len(await get_all_merch()) + 1
    category = user_dict[message.chat.id]['create_category']
    product = user_dict[message.chat.id]['create_product']
    title = user_dict[message.chat.id]['create_title']
    amount = user_dict[message.chat.id]['create_amount']
    data = {"id_merch": id_merch, "category": category, "product": product,
            "title": title, "image": photo, 'amount': amount}
    await add_merch(data=data)
    await message.answer(text='Merch успешно добавлен в базу')
    await state.set_state(default_state)
    await state.clear()
