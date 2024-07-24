from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, or_f, CommandObject
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.utils.deep_linking import create_start_link, decode_payload
from keyboards.keyboard_user import keyboards_main, keyboards_get_contact, keyboard_confirm_phone, \
    keyboard_confirm_order, keyboard_confirm_pay, keyboards_card_merch_new, keyboard_create_merch, keyboard_pay_custom, \
    keyboard_size_hoodie, keyboard_size_hoodie1, keyboard_select_pay_method
from config_data.config import Config, load_config
from database.requests import get_merch, get_all_order, add_order, add_user, update_name_user, \
    update_phone_user, update_address_delivery_user, update_address_delivery_order, get_user, get_order, \
    get_merch_category, update_user_data, update_size_order, get_merch_product
from datetime import datetime
from cryptoh.XRocketAPI import XRocketPayStatus, XRocketPayCurrency, x_roket_pay
from cryptoh.CryptoBotAPI import CryptoBotPayCurrency, crypto_bot_api
from cryptoh.nanoton import from_nano, to_nano
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
async def process_start_command_user(message: Message, state: FSMContext, command: CommandObject) -> None:
    """
    Запуск бота пользователем (ввод команды /start)
    """
    logging.info(f"process_start_command_user {message.chat.id}")
    await state.set_state(default_state)
    args = command.args
    if args:
        referer_id = int(decode_payload(args))
        data = {"id_tg": message.chat.id, "username": message.from_user.username, "name": message.from_user.first_name,
                "phone": "None", "address_delivery": "None", "referer_id": referer_id}
    else:
        data = {"id_tg": message.chat.id, "username": message.from_user.username, "name": message.from_user.first_name,
                "phone": "None", "address_delivery": "None"}
    await add_user(data=data)
    await message.answer(text=f'Привет! Мы - команда One🫶🏻\n\n'
                              f'У нас отлично получается создавать стильный и качественный мерч, который мы быстро'
                              f' и бесплатно доставим в любой город СНГ от 3 до 15 дней💙',
                         reply_markup=keyboards_main())


@router.message(F.text == 'support 💙')
async def press_button_support(message: Message, state: FSMContext) -> None:
    """
    Запрос поддержки
    """
    logging.info("press_button_support")
    await state.set_state(default_state)
    await message.answer(text=f'Если у вас возникли вопросы то вы можете написать менеджеру {config.tg_bot.support}')


@router.message(F.text == 'community 👨‍🎤')
async def press_button_support(message: Message, state: FSMContext) -> None:
    """
    ссылка на канал
    """
    logging.info("press_button_support")
    await state.set_state(default_state)
    await message.answer(text=f'Переходите в нашу группу. Там вы найдете много полезной информации'
                              f' {config.tg_bot.community}')


# @router.message(F.text == 'anon merch 🎱')
# async def press_button_anon_category(message: Message, state: FSMContext) -> None:
#     logging.info("press_button_anon_category")
#     await state.set_state(default_state)
#     await message.answer(text=f'20% от каждого заказа этой категории мы отправим моментально на кошелек'
#                               f' казначейства проекта 🖤')
#     await state.update_data(category='anon')
#     await show_merch_slider(message=message, state=state)

# @router.message(F.text == 'referral program 💵🥂')
# async def press_button_referal(message: Message, state: FSMContext) -> None:
#     """
#     Получение реф ссылки
#     """
#     logging.info("press_button_referal")
#     await state.set_state(default_state)
#     await message.answer(text=f'Размести торговую карточку в своем комьюнити/группе и получай комиссию 20% с каждой'
#                               f' покупки моментально на свой кошелек 😉',
#                          reply_markup=keyboard_referal())


# @router.callback_query(F.data.startswith('referal'))
# async def process_referal(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     logging.info(f'process_referal: {callback.message.chat.id}')
#     link = await get_referral_link(callback.message.from_user.id)
#     await callback.message.answer(text=f'Ваша реферальная ссылка:\n'
#                                        f'{link}')


@router.message(F.text == 'hoodie 👘')
async def select_category_hoodie(message: Message, state: FSMContext):
    logging.info(f'select_category: {message.chat.id}')
    await state.update_data(category='hoodie')
    await show_merch_slider(message=message, state=state)


@router.message(F.text == 'cup ☕️')
async def select_category_cup(message: Message, state: FSMContext):
    logging.info(f'select_category_cup: {message.chat.id}')
    await state.update_data(category='cup')
    await show_merch_slider(message=message, state=state)


@router.message(F.text == 'flag 🚩')
async def select_category_flag(message: Message, state: FSMContext):
    logging.info(f'select_category_flag: {message.chat.id}')
    await state.update_data(category='flag')
    await show_merch_slider(message=message, state=state)


@router.message(F.text == 'T-shirt 👕👚')
async def select_category_tshirt(message: Message, state: FSMContext):
    logging.info(f'select_category_tshirt: {message.chat.id}')
    await state.update_data(category='tshirt')
    await show_merch_slider(message=message, state=state)


@router.message(F.text == 'BOXES 🎁')
async def select_category_boxes(message: Message, state: FSMContext):
    logging.info(f'select_category_boxes: {message.chat.id}')
    await state.update_data(category='boxes')
    await show_merch_slider(message=message, state=state)


# @router.message(F.text == 'create your merch 🎨')
# async def select_category_hoodie(message: Message):
#     logging.info(f'select_category: {message.chat.id}')
#     await message.answer(text='На чем бы вы хотели сделать merch',
#                          reply_markup=keyboard_create_merch())


# @router.callback_query(F.data.startswith('custom_'))
# async def process_custom(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     logging.info(f'process_custom: {callback.message.chat.id}')
#     await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
#     answer = callback.data.split('_')[1]
#     if answer == 'hoodie':
#         await state.update_data(id_merch=4)
#     elif answer == 'cup':
#         await state.update_data(id_merch=5)
#     elif answer == 'flag':
#         await state.update_data(id_merch=17)
#     await callback.message.answer(text='Отлично теперь пришли фото или файл')
#     await state.set_state(Merch.custom)


# @router.message(or_f(F.document, F.photo), StateFilter(Merch.custom))
# async def get_file_custom(message: Message, bot: Bot, state: FSMContext):
#     logging.info(f'get_file_custom: {message.chat.id}')
#     if message.photo:
#         i = 0
#         for admin_id in config.tg_bot.admin_ids.split(','):
#             try:
#                 await bot.send_photo(chat_id=admin_id,
#                                      photo=message.photo[-1].file_id,
#                                      caption=f'Пользователь @{message.from_user.username} прислал фото для кастомного мерча')
#                 i += 1
#                 if i == 1:
#                     await message.answer(text='Фото успешно отправлено менеджеру, осталось оплатить',
#                                          reply_markup=keyboard_pay_custom())
#             except:
#                 await message.answer(text='Фото не отправлено, обратитесь в поддержку')
#     if message.document:
#         i = 0
#         for admin_id in config.tg_bot.admin_ids.split(','):
#             try:
#                 await bot.send_document(chat_id=admin_id,
#                                         document=message.document.file_id,
#                                         caption=f'Пользователь @{message.from_user.username} прислал файл для кастомного мерча')
#                 i += 1
#                 if i == 1:
#                     await message.answer(text='Фото успешно отправлено менеджеру, осталось оплатить',
#                                          reply_markup=keyboard_pay_custom())
#             except:
#                 await message.answer(text='Фото не отправлено, обратитесь в поддержку')


# @router.callback_query(F.data.startswith('create_pay'))
# @router.callback_query(F.data.startswith('size1_'))
# async def process_create_pay(callback: CallbackQuery, state: FSMContext, bot: Bot):
#     """
#     Обработка оплаты товара (если товар требует выбор размера 'hoodie', 'tshirt', 'boxes', то выбираем размер)
#     :param callback:
#     :param state:
#     :param bot:
#     :return:
#     """
#     logging.info(f'process_bay_merch: {callback.message.chat.id}')
#     await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
#     user_dict[callback.message.chat.id] = await state.get_data()
#     id_merch = user_dict[callback.message.chat.id]['id_merch']
#     if not callback.data.startswith('size1'):
#         await state.set_state(default_state)
#         info_merch = await get_merch(id_merch=id_merch)
#         if info_merch.product in ['hoodie', 'tshirt', 'boxes']:
#             await callback.message.answer(text=f'Выберите размер {info_merch.product}',
#                                           reply_markup=keyboard_size_hoodie1())
#             return
#     else:
#         size = callback.data.split('_')[1]
#         await state.update_data(size=size)
#
#     # !!! REPLACE TEST AMOUNT TO
#     merch = await get_merch(id_merch=id_merch)
#     amount = merch.amount / int(config.tg_bot.test_amount)
#     invoice_id, link = await x_roket_pay.create_invoice(amount, currency=XRocketPayCurrency.ton,
#                                                         description='Pay for our merch!')
#
#     await update_user_data(**{
#         'id_tg': callback.message.chat.id,
#         'invoice_id': invoice_id,
#         'status': XRocketPayStatus.active
#     })
#
#     await callback.message.answer(f'Оплатите товар по <a href="{link}">ссылке</a>',
#                                   reply_markup=keyboard_confirm_pay(id_merch),
#                                   parse_mode='html')


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
    # models_merch = await get_merch_category(category_merch=category)
    models_merch = await get_merch_product(product_merch=category)
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
    # models_merch = await get_merch_category(category_merch=category)
    models_merch = await get_merch_product(product_merch=category)
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
    # models_merch = await get_merch_category(category_merch=category)
    models_merch = await get_merch_product(product_merch=category)
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
@router.callback_query(F.data.startswith('size_'))
async def process_bay_merch(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработка оплаты товара
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info(f'process_bay_merch: {callback.message.chat.id}')
    # удаляем сообщение вызвавшее коллбек
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    # если коллбек получен не из клавиатуры с выбором размера
    if not callback.data.startswith('size'):
        await state.set_state(default_state)
        # получаем id merch
        id_merch = int(callback.data.split('_')[1])
        # сохраняем в state значение id merch
        await state.update_data(id_merch=id_merch)
        # получаем информацию о merch из БД
        info_merch = await get_merch(id_merch=id_merch)
        # если продукт выбранного merch что-то из списка
        if info_merch.product in ['hoodie', 'tshirt', 'boxes']:
            # то предлагаем пользователю выбрать размер
            # если выбранный товар это boxes
            if info_merch.product == 'boxes':
                await callback.message.answer(text=f'Выберите размер одежды',
                                              reply_markup=keyboard_size_hoodie())
                return
            else:
                await callback.message.answer(text=f'Выберите размер {info_merch.product}',
                                              reply_markup=keyboard_size_hoodie())
                return
    # если коллбек вызван из клавиатуры выбора размера
    else:
        # получаем размер выбранного товара
        size = callback.data.split('_')[1]
        # сохраняем его в state
        await state.update_data(size=size)
        # user_dict[callback.message.chat.id] = await state.get_data()
        # id_order = user_dict[callback.message.chat.id]['id_order']
        # await update_size_order(id_order=id_order, size=size)
    # формируем оплату
    user_dict[callback.message.chat.id] = await state.get_data()
    # получаем id merch из state
    id_merch = user_dict[callback.message.chat.id]['id_merch']
    # получаем информацию о товаре по его id
    merch = await get_merch(id_merch=id_merch)
    # формируем стоимость для оплаты
    amount = merch.amount / int(config.tg_bot.test_amount)
    await state.set_state(default_state)
    # сохраняем в state стоимость
    await state.update_data(amount=amount)
    # выбор метода оплаты
    await callback.message.answer('Выберите метод оплаты:', reply_markup=keyboard_select_pay_method())


@router.callback_query(F.data.startswith('pay_method_'))
async def process_pay_method(callback: CallbackQuery, state: FSMContext):
    # !!! ВОТ НА ЭТОМ ЭТАПЕ МЕРЧ ВЫБРАН СУММА К ОПЛАТЕ ЕСТЬ НУЖНО ВЫБРАТЬ СПОСОБ ОПЛАТЫ
    await callback.answer('')

    method = callback.data.split('_')[-1]

    invoice_id, link, pay_method = None, None, None

    data = await state.get_data()

    # match method:
    if method == 'C':
        invoice_id, link = await crypto_bot_api.create_invoice(amount=data['amount'],
                                                               currency=CryptoBotPayCurrency.ton,
                                                               description='Pay for our merch!')
        pay_method = 'CryptoBot'

    if method == 'X':
        invoice_id, link = await x_roket_pay.create_invoice(amount=data['amount'], currency=XRocketPayCurrency.ton,
                                                            description='Pay for our merch!')
        pay_method = 'XRocketBot'

    if method == 'P':
        pay_method = 'Passed'
        await callback.message.answer('Отмена..', reply_markup=keyboards_main())
        await state.clear()
        return
    if method == "_":
        pass

    await update_user_data(**{
        'id_tg': callback.message.chat.id,
        'invoice_id': invoice_id,
        'status': XRocketPayStatus.active,
        'pay_method': pay_method,
    })

    await callback.message.answer(f'Оплатите товар по <a href="{link}">ссылке</a>',
                                  reply_markup=keyboard_confirm_pay(data["id_merch"]),
                                  parse_mode='html')


@router.callback_query(F.data.startswith('confirm_pay_for_'))
async def process_paying(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info('Processing_paying')
    await callback.answer()
    # обновляем словарь из state
    user_dict[callback.message.chat.id] = await state.get_data()
    # получаем id merch
    id_merch = user_dict[callback.message.chat.id]['id_merch']
    # производим проверку оплаты пользователем
    invoice_id = (await get_user(callback.from_user.id)).invoice_id
    pay_method = (await get_user(callback.from_user.id)).pay_method
    # получаем статус оплаты
    status = await x_roket_pay.check_invoice_payed(invoice_id) if pay_method.startswith(
        'X') else await crypto_bot_api.check_invoice_paid(invoice_id)
    logging.info(f"get_{pay_method}_invoice_{invoice_id}_status: {status} to {callback.from_user.id}")

    if status:
        pay = True
        await update_user_data(**{
            'id_tg': callback.message.chat.id,
            'invoice_id': 0,
            'status': XRocketPayStatus.passed
        })
    else:
        pay = False
    # если оплата прошла успешно
    pay = True
    if pay:
        # информируем пользователя
        await callback.message.answer(text='Оплата прошла успешно')
        # формируем id заказа как количество всех заказов + 1
        count_order = len(await get_all_order()) + 1
        # получаем информацию о мерч по его id
        info_merch = await get_merch(id_merch=id_merch)
        logging.info(f"amount: {info_merch.amount * 0.2 / int(config.tg_bot.test_amount)}")
        # если категория продукта не anon то отправляем комиссию рефереру который пригласил пользователя
        if not info_merch.category == 'anon':
            # если реферер у пользователя есть
            if (not (await get_user(id_tg=callback.message.chat.id)).referer_id == 0) and \
                    (not (await get_user(id_tg=callback.message.chat.id)).referer_id == None):
                # перевод комиссии по id реферера
                await x_roket_pay.transfer_funds_with_id(
                    amount=info_merch.amount * 0.2 / int(config.tg_bot.test_amount),
                    user_id=(await get_user(id_tg=callback.message.chat.id)).referer_id
                )
                # информируем админа об отправке комиссии
                for admin_id in config.tg_bot.admin_ids.split(','):
                    try:
                        await bot.send_message(chat_id=int(admin_id),
                                               text=f'Отправляем 20% {info_merch.amount * 0.2} TON '
                                                    f'{(await get_user(id_tg=callback.message.chat.id)).referer_id}')
                    except:
                        pass
        # иначе производим перечисление комиссии на кошелек anon
        else:
            # !!! перевод комиссии на кошелек за приобретение merch anon
            await x_roket_pay.transfer_funds_with_wallet_addr(
                amount=info_merch.amount * 0.2,
                wallet_addr='EQDBAsSdj5riEKYx42fyJMQIIo2hwcCA5aezuGCBrx-tT2SW'
            )
            # информируем админа о переводе комисии
            for admin_id in config.tg_bot.admin_ids.split(','):
                try:
                    await bot.send_message(chat_id=int(admin_id),
                                           text=f'Отправляем в казначейство anon 20% {info_merch.amount * 0.2} TON')

                except:
                    pass
        # формируем заказ в БД
        await state.update_data(id_order=count_order)
        # если продукт это что-то из списка то получаем разсер
        if info_merch.product in ['hoodie', 'tshirt', 'boxes']:
            size = user_dict[callback.message.chat.id]['size']
        else:
            size = "None"
        # формируем словарь для оплаты
        data = {"id_order": count_order, "id_tg": callback.message.chat.id, "id_merch": id_merch, "size": size,
                "count": 1, "cost": info_merch.amount, "address_delivery": "None",
                "date_order": datetime.today().strftime('%d/%m/%Y')}
        # добавляем заказ в БД
        await add_order(data=data)
        # запрос ввода адреса отправки merch
        await callback.message.answer(
            text=f'Для точной доставки нам нужны данные получателя: фио, телефон для уведомления,'
                 f' адрес и город, наш партнер по доставке CDEK ✅',
            reply_markup=keyboards_main())
        # ожидаем ввод пользователя
        await state.set_state(Merch.address_delivery)
    else:
        await callback.message.answer(text='Оплата не прошла. Повторите попытку')
        await state.set_state(default_state)


# @router.callback_query(F.data.startswith('size_'))
# async def get_size_hoodie(callback: CallbackQuery, state: FSMContext):
#     logging.info('get_size_hoodie')
#     await callback.answer()
#     size = callback.data.split('_')[1]
#     await state.update_data(size=size)
#     user_dict[callback.message.chat.id] = await state.get_data()
#     id_order = user_dict[callback.message.chat.id]['id_order']
#     await update_size_order(id_order=id_order, size=size)
#     await callback.message.answer(text=f'Как вас зовут?')
#     await state.set_state(Merch.username)


@router.callback_query(F.data.startswith('cancel_pay_for_'))
async def cancel_pay_for(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await callback.answer('Отменено', show_alert=True)
    await state.clear()


# @router.message(F.text, Merch.username)
# async def get_username(message: Message, state: FSMContext):
#     """Получаем имя пользователя. Запрашиваем номер телефона"""
#     logging.info(f'get_username: {message.from_user.id}')
#     name = message.text
#     await state.update_data(name=name)
#     await update_name_user(id_tg=message.chat.id, name=name)
#     await message.answer(text=f'Рад вас приветствовать {name}. Поделитесь вашим номером телефона ☎️',
#                          reply_markup=keyboards_get_contact())
#     await state.set_state(Merch.phone)


# @router.message(or_f(F.text, F.contact), StateFilter(Merch.phone))
# async def process_validate_russian_phone_number(message: Message, state: FSMContext) -> None:
#     """Получаем номер телефона пользователя (проводим его валидацию). Подтверждаем введенные данные"""
#     logging.info("process_validate_russian_phone_number")
#     if message.contact:
#         phone = str(message.contact.phone_number)
#     else:
#         phone = message.text
#         if not validate_russian_phone_number(phone):
#             await message.answer(text="Неверный формат номера. Повторите ввод, например 89991112222:")
#             return
#     await state.update_data(phone=phone)
#     await update_phone_user(id_tg=message.chat.id, phone=phone)
#     await state.set_state(default_state)
#     await message.answer(text=f'Записываю, {phone}. Верно?',
#                          reply_markup=keyboard_confirm_phone())


# @router.callback_query(F.data == 'get_phone_back')
# async def process_get_phone_back(callback: CallbackQuery, state: FSMContext) -> None:
#     """Изменение введенного номера телефона"""
#     logging.info(f'process_get_phone_back: {callback.message.chat.id}')
#     await callback.message.edit_text(text=f'Поделитесь вашим номером телефона ☎️',
#                                      reply_markup=None)
#     await state.set_state(Merch.phone)


# @router.callback_query(F.data == 'confirm_phone')
# async def process_confirm_phone(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
#     """Введенный номер телефона подтвержден. Запрос города"""
#     logging.info(f'process_confirm_phone: {callback.message.chat.id}')
#     await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
#     await callback.message.answer(text=f'Для точной доставки нам нужны данные получителя: фио, телефон для уведомления,'
#                                        f' адрес и город, наш партнер по доставке CDEK ✅',
#                                   reply_markup=keyboards_main())
#     await state.set_state(Merch.address_delivery)


@router.message(F.text, Merch.address_delivery)
async def get_address_delivery(message: Message, state: FSMContext, bot: Bot):
    """Получаем имя пользователя. Запрашиваем номер телефона"""
    logging.info(f'get_address_delivery: {message.from_user.id}')
    # данные о доставке от пользователя
    info_contact = message.text
    # запоминаем в state контактные данные
    await state.update_data(address_delivery=info_contact)
    # заносим контактные данные в БД в таблицу пользователя
    await update_address_delivery_user(id_tg=message.chat.id, address_delivery=info_contact)
    # обновляем словарь данных пользователя
    user_dict[message.chat.id] = await state.get_data()
    # получаем id заказа
    id_order = user_dict[message.chat.id]['id_order']
    # заносим контактные данные в БД в таблицу заказов
    await update_address_delivery_order(id_order=id_order, address_delivery=info_contact)
    # id_merch = user_dict[message.chat.id]['id_merch']
    # name = user_dict[message.chat.id]['name']
    # phone = user_dict[message.chat.id]['phone']
    # address_delivery = user_dict[message.chat.id]['address_delivery']
    # id_order = user_dict[message.chat.id]['id_order']
    # await update_address_delivery_order(id_order=id_order, address_delivery=info_contact)
    # merch_info = await get_merch(id_merch=id_merch)
    # await message.answer(text=f'<b>{name}, проверьте данные:</b>\n'
    #                           f'<i>Merch:</i> {merch_info.title} - {merch_info.amount} TON\n'
    #                           f'<i>Ваш телефон:</i> {phone}\n'
    #                           f'<i>Адрес доставки:</i> {address_delivery}.\n'
    #                           f'Верно?',
    #                      reply_markup=keyboard_confirm_order(id_order=id_order),
    #                      parse_mode='html')

    # async def get_address_delivery_1(message: Message, state: FSMContext):
    #     """
    #     Если пользователь подтвердил ранее введенные данные
    #     :param message:
    #     :param state:
    #     :return:
    #     """
    #     logging.info(f'get_address_delivery: {message.chat.id}')
    #     user_info = await get_user(id_tg=message.chat.id)
    #     user_dict[message.chat.id] = await state.get_data()
    #     id_merch = user_dict[message.chat.id]['id_merch']
    #     id_order = user_dict[message.chat.id]['id_order']
    #     merch_info = await get_merch(id_merch=id_merch)
    #
    #     await message.answer(text=f'<b>{user_info.name}, проверьте данные:</b>\n'
    #                               f'<i>Merch:</i> {merch_info.title} - {merch_info.amount} TON\n'
    #                               f'<i>Ваш телефон:</i> {user_info.phone}\n'
    #                               f'<i>Адрес доставки:</i> {user_info.address_delivery}.\n'
    #                               f'Верно?',
    #                          reply_markup=keyboard_confirm_order(id_order=id_order),
    #                          parse_mode='html')
    #
    #
    # @router.callback_query(F.data.startswith("order_"))
    # async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    #     """
    #     Подтверждение заказ
    #     :param callback:
    #     :param state:
    #     :return:
    #     """
    #     logging.info(f'confirm_order: {callback.message.chat.id}')
    #     answer = callback.data.split('_')[1]
    #     if answer == 'cancel':
    #         await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    #         await callback.message.answer(text='Данные не подтверждены, повторите ввод')
    #         await get_username(message=callback.message, state=state)
    #     elif answer == 'confirm':
    #         await callback.answer(text='Данные подтверждены',
    #                               show_alert=True)
    #         user_dict[callback.message.chat.id] = await state.get_data()
    # получаем id заказанного товара
    id_merch = user_dict[message.chat.id]['id_merch']
    #         id_order = user_dict[callback.message.chat.id]['id_order']
    # получаем информацию о пользователе
    user_info = await get_user(id_tg=message.chat.id)
    #         address_delivery = user_info.address_delivery
    # получаем информацию о товаре
    merch_info = await get_merch(id_merch=id_merch)
    # получаем информацию о заказе
    order_info = await get_order(id_order=id_order)
    # отправляем пользователю благодарность
    await message.answer(text=f'Благодарим вас за заказ!\n'
                              f'Наш merch {merch_info.title} уже мчит к вам '
                              f'{order_info.address_delivery}.',
                         reply_markup=None)
    # информируем админа об оплаченном заказе для его отправки пользователю
    for admin_id in config.tg_bot.admin_ids.split(','):
        try:
            if merch_info.product in ['hoodie', 'tshirt', 'boxes']:
                size = order_info.size
                await bot.send_message(chat_id=int(admin_id),
                                       text=f'<b>Заказ № {order_info.id_order}:</b>\n'
                                            f'<i>Заказчик:</i> {user_info.name} / @{user_info.username}\n'
                                            f'<i>Мерч:</i> {merch_info.title}\n'
                                            f'<i>Размер:</i> {size}\n'
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

