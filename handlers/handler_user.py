from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, or_f
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state

from keyboards.keyboard_user import keyboards_main, keyboards_get_contact, keyboard_confirm_phone, \
    keyboard_confirm_order, keyboard_confirm_pay, keyboards_card_merch_new, keyboard_create_merch, keyboard_pay_custom
from config_data.config import Config, load_config
from database.requests import get_merch, get_all_order, add_order, add_user, update_name_user,\
    update_phone_user, update_address_delivery_user, update_address_delivery_order, get_user, get_order,\
    get_merch_category, update_user_data
from filter.filter import validate_russian_phone_number
from cryptoh.CryptoHelper import XRocketPayStatus, XRocketPayCurrency, x_roket_pay


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

@router.message(CommandStart())
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    """
    Запуск бота пользователем (ввод команды /start)
    """
    logging.info(f"process_start_command_user {message.chat.id}")
    await state.set_state(default_state)

    data = {"id_tg": message.chat.id, "username": message.from_user.username, "name": message.from_user.first_name,
            "phone": "None", "address_delivery": "None"}
    await add_user(data=data)
    await message.answer(text=f'Приветственное сообщение. Рассказ о том что может этот бот и краткая инструкция'
                              f' как им пользоваться.\n'
                              f'Если возникли сложности или вопросы то можете обратиться в поддержку',
                         reply_markup=keyboards_main())


@router.message(F.text == 'Поддержка')
async def press_button_support(message: Message, state: FSMContext) -> None:
    """
    Запрос поддержки
    """
    logging.info("press_button_support")
    await state.set_state(default_state)
    await message.answer(text=f'Если у вас возникли вопросы то вы можете написать менеджеру {config.tg_bot.support}')


@router.message(F.text == 'hoodie')
async def select_category_hoodie(message: Message, state: FSMContext):
    logging.info(f'select_category: {message.chat.id}')
    await state.update_data(category='hoodie')
    await show_merch_slider(message=message, state=state)


@router.message(F.text == 'cup')
async def select_category_hoodie(message: Message, state: FSMContext):
    logging.info(f'select_category: {message.chat.id}')
    await state.update_data(category='cup')
    await show_merch_slider(message=message, state=state)


@router.message(F.text == 'create your merch')
async def select_category_hoodie(message: Message):
    logging.info(f'select_category: {message.chat.id}')
    await message.answer(text='На чем бы вы хотели сделать merch',
                         reply_markup=keyboard_create_merch())


@router.callback_query(F.data.startswith('custom_'))
async def process_custom(callback: CallbackQuery, state: FSMContext):
    logging.info(f'process_custom: {callback.message.chat.id}')
    answer = callback.data.split('_')[1]
    if answer == 'hoodie':
        await state.update_data(id_merch=7)
    elif answer == 'cup':
        await state.update_data(id_merch=8)
    await callback.message.answer(text='Отлично теперь пришли фото или файл')
    await state.set_state(Merch.custom)


@router.message(or_f(F.document, F.photo), StateFilter(Merch.custom))
async def get_file_custom(message: Message, bot: Bot, state: FSMContext):
    logging.info(f'get_file_custom: {message.chat.id}')
    if message.photo:
        try:
            await bot.send_photo(chat_id=config.tg_bot.admin_ids,
                                 photo=message.photo[-1].file_id,
                                 caption=f'Пользователь @{message.from_user.username} прислал фото для кастомного мерча')
            await message.answer(text='Фото успешно отправлено менеджеру, осталось оплатить',
                                 reply_markup=keyboard_pay_custom())

        except:
            await message.answer(text='Фото не отправлено, обратитесь в поддержку')
    if message.document:
        try:
            await bot.send_document(chat_id=config.tg_bot.admin_ids,
                                    document=message.document.file_id,
                                    caption=f'Пользователь @{message.from_user.username} прислал файл для кастомного мерча')
            await message.answer(text='Фото успешно отправлено менеджеру, осталось оплатить',
                                 reply_markup=keyboard_pay_custom())
        except:
            await message.answer(text='Фото не отправлено, обратитесь в поддержку')


@router.callback_query(F.data.startswith('create_pay'))
async def process_create_pay(callback: CallbackQuery, state: FSMContext):
    """
    Обработка оплаты товара
    :param callback:
    :param state:
    :return:
    """
    logging.info(f'process_bay_merch: {callback.message.chat.id}')
    await state.set_state(default_state)
    user_dict[callback.message.chat.id] = await state.get_data()
    id_merch = user_dict[callback.message.chat.id]['id_merch']
    # !!! REPLACE TEST AMOUNT TO
    merch = await get_merch(id_merch=id_merch)
    amount = merch.amount / 10000
    invoice_id, link = await x_roket_pay.create_invoice(amount, currency=XRocketPayCurrency.ton,
                                                        description='📄 Pay for our merch!')

    await update_user_data(**{
        'id_tg': callback.message.chat.id,
        'invoice_id': invoice_id,
        'status': XRocketPayStatus.active
    })

    await callback.message.answer(f'Оплатите товар по <a href="{link}">ссылке</a>',
                                  reply_markup=keyboard_confirm_pay(id_merch),
                                  parse_mode='html')


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


@router.callback_query(F.data.startswith('bay_'))
async def process_bay_merch(callback: CallbackQuery, state: FSMContext):
    """
    Обработка оплаты товара
    :param callback:
    :param state:
    :return:
    """
    logging.info(f'process_bay_merch: {callback.message.chat.id}')
    await state.set_state(default_state)
    id_merch = int(callback.data.split('_')[1])
    await state.update_data(id_merch=id_merch)
    # !!! REPLACE TEST AMOUNT TO
    merch = await get_merch(id_merch=id_merch)
    amount = merch.amount / 10000
    invoice_id, link = await x_roket_pay.create_invoice(amount, currency=XRocketPayCurrency.ton,
                                                        description='📄 Pay for our merch!')

    await update_user_data(**{
        'id_tg': callback.message.chat.id,
        'invoice_id': invoice_id,
        'status': XRocketPayStatus.active
    })

    await callback.message.answer(f'Оплатите товар по <a href="{link}">ссылке</a>',
                                  reply_markup=keyboard_confirm_pay(id_merch),
                                  parse_mode='html')


@router.callback_query(F.data.startswith('confirm_pay_for_'))
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
        await state.update_data(id_order=count_order)
        # if await get_user(id_tg=callback.message.chat.id):
        #     user = await get_user(id_tg=callback.message.chat.id)
        #     data = {"id_order": count_order, "id_tg": callback.message.chat.id, "id_merch": id_merch, "count": 1,
        #             "cost": info_merch.amount, "address_delivery": user.address_delivery}
        #     await add_order(data=data)
        #     await get_address_delivery_1(message=callback.message, state=state)
        # else:
        data = {"id_order": count_order, "id_tg": callback.message.chat.id, "id_merch": id_merch, "count": 1,
                "cost": info_merch.amount, "address_delivery": "None"}
        await add_order(data=data)
        await callback.message.answer(text=f'Как вас зовут?')
        await state.set_state(Merch.username)
    else:
        await callback.message.answer(text='Оплата не прошла. Повторите попытку')
        await state.set_state(default_state)


@router.callback_query(F.data.startswith('cancel_pay_for_'))
async def cancel_pay_for(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отменено', show_alert=True)
    await state.clear()


@router.message(F.text, Merch.username)
async def get_username(message: Message, state: FSMContext):
    """Получаем имя пользователя. Запрашиваем номер телефона"""
    logging.info(f'get_username: {message.from_user.id}')
    name = message.text
    await state.update_data(name=name)
    await update_name_user(id_tg=message.chat.id, name=name)
    await message.answer(text=f'Рад вас приветствовать {name}. Поделитесь вашим номером телефона ☎️',
                         reply_markup=keyboards_get_contact())
    await state.set_state(Merch.phone)


@router.message(or_f(F.text, F.contact), StateFilter(Merch.phone))
async def process_validate_russian_phone_number(message: Message, state: FSMContext) -> None:
    """Получаем номер телефона пользователя (проводим его валидацию). Подтверждаем введенные данные"""
    logging.info("process_validate_russian_phone_number")
    if message.contact:
        phone = str(message.contact.phone_number)
    else:
        phone = message.text
        if not validate_russian_phone_number(phone):
            await message.answer(text="Неверный формат номера. Повторите ввод, например 89991112222:")
            return
    await state.update_data(phone=phone)
    await update_phone_user(id_tg=message.chat.id, phone=phone)
    await state.set_state(default_state)
    await message.answer(text=f'Записываю, {phone}. Верно?',
                         reply_markup=keyboard_confirm_phone())


@router.callback_query(F.data == 'get_phone_back')
async def process_get_phone_back(callback: CallbackQuery, state: FSMContext) -> None:
    """Изменение введенного номера телефона"""
    logging.info(f'process_get_phone_back: {callback.message.chat.id}')
    await callback.message.edit_text(text=f'Поделитесь вашим номером телефона ☎️',
                                     reply_markup=None)
    await state.set_state(Merch.phone)


@router.callback_query(F.data == 'confirm_phone')
async def process_confirm_phone(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """Введенный номер телефона подтвержден. Запрос города"""
    logging.info(f'process_confirm_phone: {callback.message.chat.id}')
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.message.answer(text=f'Укажите адрес доставки',
                                  reply_markup=keyboards_main())
    await state.set_state(Merch.address_delivery)


@router.message(F.text, Merch.address_delivery)
async def get_address_delivery(message: Message, state: FSMContext):
    """Получаем имя пользователя. Запрашиваем номер телефона"""
    logging.info(f'get_address_delivery: {message.from_user.id}')
    address_delivery = message.text
    await state.update_data(address_delivery=address_delivery)
    await update_address_delivery_user(id_tg=message.chat.id, address_delivery=address_delivery)

    user_dict[message.chat.id] = await state.get_data()
    id_merch = user_dict[message.chat.id]['id_merch']
    name = user_dict[message.chat.id]['name']
    phone = user_dict[message.chat.id]['phone']
    address_delivery = user_dict[message.chat.id]['address_delivery']
    id_order = user_dict[message.chat.id]['id_order']
    await update_address_delivery_order(id_order=id_order, address_delivery=address_delivery)
    merch_info = await get_merch(id_merch=id_merch)
    await message.answer(text=f'<b>{name}, проверьте данные:</b>\n'
                              f'<i>Merch:</i> {merch_info.title} - {merch_info.amount} TON\n'
                              f'<i>Ваш телефон:</i> {phone}\n'
                              f'<i>Адрес доставки:</i> {address_delivery}.\n'
                              f'Верно?',
                         reply_markup=keyboard_confirm_order(id_order=id_order),
                         parse_mode='html')


async def get_address_delivery_1(message: Message, state: FSMContext):
    """
    Если пользователь подтвердил ранее введенные данные
    :param message:
    :param state:
    :return:
    """
    logging.info(f'get_address_delivery: {message.chat.id}')
    user_info = await get_user(id_tg=message.chat.id)
    user_dict[message.chat.id] = await state.get_data()
    id_merch = user_dict[message.chat.id]['id_merch']
    id_order = user_dict[message.chat.id]['id_order']
    merch_info = await get_merch(id_merch=id_merch)

    await message.answer(text=f'<b>{user_info.name}, проверьте данные:</b>\n'
                              f'<i>Merch:</i> {merch_info.title} - {merch_info.amount} TON\n'
                              f'<i>Ваш телефон:</i> {user_info.phone}\n'
                              f'<i>Адрес доставки:</i> {user_info.address_delivery}.\n'
                              f'Верно?',
                         reply_markup=keyboard_confirm_order(id_order=id_order),
                         parse_mode='html')


@router.callback_query(F.data.startswith("order_"))
async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Подтверждение заказ
    :param callback:
    :param state:
    :return:
    """
    logging.info(f'confirm_order: {callback.message.chat.id}')
    answer = callback.data.split('_')[1]
    if answer == 'cancel':
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer(text='Данные не подтверждены, повторите ввод')
        await get_username(message=callback.message, state=state)
    elif answer == 'confirm':
        await callback.answer(text='Данные подтверждены',
                              show_alert=True)
        user_dict[callback.message.chat.id] = await state.get_data()
        id_merch = user_dict[callback.message.chat.id]['id_merch']
        id_order = user_dict[callback.message.chat.id]['id_order']
        user_info = await get_user(id_tg=callback.message.chat.id)
        address_delivery = user_info.address_delivery
        merch_info = await get_merch(id_merch=id_merch)
        order_info = await get_order(id_order=id_order)
        await callback.message.edit_text(text=f'Благодарим вас за заказ!\n'
                                              f'Наш merch {merch_info.title} уже мчит к вам на адрес '
                                              f'{address_delivery}.',
                                         reply_markup=None)
        for admin_id in config.tg_bot.admin_ids.split(','):
            try:
                await bot.send_message(chat_id=admin_id,
                                       text=f'<b>Заказ № {order_info.id_order}:</b>\n'
                                            f'<i>Заказчик:</i> {user_info.name} / @{user_info.username}\n'
                                            f'<i>Номер телефона</i>: {user_info.phone}\n'
                                            f'<i>Мерч:</i> {merch_info.title}\n'
                                            f'<i>Адрес:</i> {order_info.address_delivery}',
                                       parse_mode='html')
            except:
                pass
        await state.set_state(default_state)

