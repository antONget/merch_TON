from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, or_f
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from keyboards.keyboard_anon_merch import keyboards_card_merch_anon, keyboard_size_hoodie_anon,\
    keyboard_confirm_pay_anon
from config_data.config import Config, load_config
from database.requests import get_merch_category, get_merch, update_user_data, get_user, get_all_order, add_order, \
    update_address_delivery_user, update_address_delivery_order, get_order
from cryptoh.CryptoHelper import XRocketPayStatus, XRocketPayCurrency, x_roket_pay
from datetime import datetime
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
    await show_merch_slider_anon(message=message, state=state)


async def show_merch_slider_anon(message: Message, state: FSMContext):
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
    keyboard = keyboards_card_merch_anon(list_merch=list_merch, block=0)
    await message.answer_photo(photo=list_merch[0].image,
                               reply_markup=keyboard)


# >>
@router.callback_query(F.data.startswith('anonforward_'))
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
    keyboard = keyboards_card_merch_anon(list_merch=list_merch, block=num_block)
    try:
        await callback.message.edit_media(media=InputMediaPhoto(media=list_merch[num_block].image),
                                          reply_markup=keyboard)
    except:
        logging.info('ERROR')


# <<
@router.callback_query(F.data.startswith('anonback_'))
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
    keyboard = keyboards_card_merch_anon(list_merch=list_merch, block=num_block)
    try:
        await callback.message.edit_media(media=InputMediaPhoto(media=list_merch[num_block].image),
                                          reply_markup=keyboard)
    except:
        logging.info('ERROR')


@router.callback_query(F.data.startswith('anonbay_'))
@router.callback_query(F.data.startswith('anonsize_'))
async def process_bay_merch(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработка оплаты товара
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_bay_merch: {callback.message.chat.id}')
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    if not callback.data.startswith('anonsize'):
        await state.set_state(default_state)
        id_merch = int(callback.data.split('_')[1])
        await state.update_data(id_merch=id_merch)
        info_merch = await get_merch(id_merch=id_merch)
        if info_merch.product == 'hoodie':
            await callback.message.answer(text=f'Выберите размер hoodie',
                                          reply_markup=keyboard_size_hoodie_anon())
            return
    user_dict[callback.message.chat.id] = await state.get_data()
    id_merch = user_dict[callback.message.chat.id]['id_merch']
    merch = await get_merch(id_merch=id_merch)
    # !!! REPLACE TEST AMOUNT TO
    amount = merch.amount / int(config.tg_bot.test_amount)
    invoice_id, link = await x_roket_pay.create_invoice(amount, currency=XRocketPayCurrency.ton,
                                                        description='Pay for our merch!')

    await update_user_data(**{
        'id_tg': callback.message.chat.id,
        'invoice_id': invoice_id,
        'status': XRocketPayStatus.active
    })

    await callback.message.answer(f'Оплатите товар по <a href="{link}">ссылке</a>',
                                  reply_markup=keyboard_confirm_pay_anon(id_merch),
                                  parse_mode='html')


@router.callback_query(F.data.startswith('anonconfirm_pay_for_'))
async def process_paying(callback: CallbackQuery, state: FSMContext):
    logging.info('Processing_paying')
    await callback.answer()
    user_dict[callback.message.chat.id] = await state.get_data()
    id_merch = user_dict[callback.message.chat.id]['id_merch']

    invoice_id = (await get_user(callback.from_user.id)).invoice_id
    status = await x_roket_pay.check_invoice_payed(invoice_id)
    logging.info(f"get_invoice_{invoice_id}_status: {status} to {callback.from_user.id}")
    if status:
        pay = True
        await update_user_data(**{
            'id_tg': callback.message.chat.id,
            'invoice_id': 0,
            'status': XRocketPayStatus.passed
        })

    else:
        pay = False
    if pay:
        await callback.message.answer(text='Оплата прошла успешно')
        count_order = len(await get_all_order()) + 1
        info_merch = await get_merch(id_merch=id_merch)
        if not info_merch.category == 'anon':
            if not (await get_user(id_tg=callback.message.chat.id)).referer_id == 0:
                # перевод комиссии по id реферера
                await callback.message.answer(text=f'Отправляем 20% {info_merch.amount * 0.2} TON'
                                                   f'{(await get_user(id_tg=callback.message.chat.id)).referer_id}')
        else:
            await callback.message.answer(text=f'Отправляем в казначейство anon 20% {info_merch.amount * 0.2} TON')
            # !!! перевод комиссии на кошелек за приобретение merch anon
        await state.update_data(id_order=count_order)
        data = {"id_order": count_order, "id_tg": callback.message.chat.id, "id_merch": id_merch, "count": 1,
                "cost": info_merch.amount, "address_delivery": "None",
                "date_order": datetime.today().strftime('%d/%m/%Y')}
        await add_order(data=data)

        await callback.message.answer(
            text=f'Для точной доставки нам нужны данные получателя: фио, телефон для уведомления,'
                 f' адрес и город, наш партнер по доставке CDEK ✅')
        await state.set_state(Merch.address_delivery)
    else:
        await callback.message.answer(text='Оплата не прошла. Повторите попытку')
        await state.set_state(default_state)


@router.callback_query(F.data.startswith('anoncancel_pay_for_'))
async def cancel_pay_for(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.answer('Отменено', show_alert=True)
    await state.clear()


@router.message(F.text, Merch.address_delivery)
async def get_address_delivery(message: Message, state: FSMContext, bot: Bot):
    """Получаем адрес и отправляем менеджеру заказ"""
    logging.info(f'get_address_delivery: {message.from_user.id}')
    info_contact = message.text
    await state.update_data(address_delivery=info_contact)
    await update_address_delivery_user(id_tg=message.chat.id, address_delivery=info_contact)
    user_dict[message.chat.id] = await state.get_data()
    id_order = user_dict[message.chat.id]['id_order']
    await update_address_delivery_order(id_order=id_order, address_delivery=info_contact)
    id_merch = user_dict[message.chat.id]['id_merch']
    user_info = await get_user(id_tg=message.chat.id)
    merch_info = await get_merch(id_merch=id_merch)
    order_info = await get_order(id_order=id_order)

    await message.answer(text=f'Благодарим вас за заказ!\n'
                              f'Наш merch {merch_info.title} уже мчит к вам на адрес '
                              f'{order_info.address_delivery}.',
                         reply_markup=None)
    for admin_id in config.tg_bot.admin_ids.split(','):
        try:
            if merch_info.category == 'hoodie':
                size = order_info.size
                await bot.send_message(chat_id=admin_id,
                                       text=f'<b>Заказ № {order_info.id_order}:</b>\n'
                                            f'<i>Заказчик:</i> {user_info.name} / @{user_info.username}\n'
                                            f'<i>Мерч:</i> {merch_info.title}\n'
                                            f'<i>Размер:</i> {size}'
                                            f'<i>Контактные данные:</i> {order_info.address_delivery}',
                                       parse_mode='html')
            else:
                await bot.send_message(chat_id=admin_id,
                                       text=f'<b>Заказ № {order_info.id_order}:</b>\n'
                                            f'<i>Заказчик:</i> {user_info.name} / @{user_info.username}\n'
                                            f'<i>Мерч:</i> {merch_info.title}\n'
                                            f'<i>Контактные данные:</i> {order_info.address_delivery}',
                                       parse_mode='html')
        except:
            pass
    await state.set_state(default_state)