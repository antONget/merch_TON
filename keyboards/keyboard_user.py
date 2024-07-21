from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_main() -> ReplyKeyboardMarkup:
    logging.info("keyboards_main")
    button_1 = KeyboardButton(text='hoodie 👘')
    button_2 = KeyboardButton(text='cup ☕️')
    button_6 = KeyboardButton(text='flag 🚩')
    # button_8 = KeyboardButton(text='anon merch 🎱')
    # button_3 = KeyboardButton(text='create your merch 🎨')
    button_4 = KeyboardButton(text='support 💙')
    button_5 = KeyboardButton(text='community 👨‍🎤')
    button_7 = KeyboardButton(text='referral program 💵🥂')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_6], [button_7],
                                             [button_4, button_5]],
                                   resize_keyboard=True)
    return keyboard


def keyboard_create_merch():
    logging.info("keyboard_create_merch")
    button_1 = InlineKeyboardButton(text='hoodie 👘',
                                    callback_data='custom_hoodie')
    button_2 = InlineKeyboardButton(text='cup ☕️',
                                    callback_data='custom_cup')
    button_3 = InlineKeyboardButton(text='flag 🚩',
                                    callback_data='custom_flag')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard


# def keyboard_refer():
#     logging.info("keyboard_refer")
#     button_1 = InlineKeyboardButton(text='Получить реферальную ссылку',
#                                     callback_data='refer')
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
#     return keyboard


def keyboard_pay_custom():
    logging.info("keyboard_pay_custom")
    button_1 = InlineKeyboardButton(text='Оплатить',
                                    callback_data='create_pay')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboards_card_merch_new(list_merch: list, block: int):
    logging.info("keyboards_card_merch")
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    text = f'Купить'
    button = f'bay_{list_merch[block].id_merch}'
    buttons.append(InlineKeyboardButton(
        text=text,
        callback_data=button))
    button_back = InlineKeyboardButton(text='<<',
                                       callback_data=f'back_{str(block)}')
    button_next = InlineKeyboardButton(text='>>',
                                       callback_data=f'forward_{str(block)}')
    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_next)
    return kb_builder.as_markup()


def keyboard_bay_merch(id_merch):
    logging.info("keyboard_confirm_cantact_date")
    button_1 = InlineKeyboardButton(text='Купить',
                                    callback_data=f'bay_{id_merch}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard


def keyboards_get_contact() -> ReplyKeyboardMarkup:
    logging.info("keyboards_get_contact")
    button_1 = KeyboardButton(text='Отправить свой контакт ☎️',
                              request_contact=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1]],
        resize_keyboard=True
    )
    return keyboard


def keyboard_confirm_phone():
    logging.info("keyboard_confirm_phone")
    button_1 = InlineKeyboardButton(text='Верно',
                                    callback_data='confirm_phone')
    button_2 = InlineKeyboardButton(text='Изменить',
                                    callback_data='get_phone_back')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]],)
    return keyboard


def keyboard_confirm_order(id_order: int):
    logging.info("confirm_pay")
    button_1 = InlineKeyboardButton(text='Подтвердить', callback_data=f'order_confirm_{id_order}')
    button_2 = InlineKeyboardButton(text='Изменить', callback_data=f'order_cancel_{id_order}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard


def keyboard_size_hoodie():
    logging.info("confirm_pay")
    button_1 = InlineKeyboardButton(text='M', callback_data=f'size_M')
    button_2 = InlineKeyboardButton(text='L', callback_data=f'size_L')
    button_3 = InlineKeyboardButton(text='XL', callback_data=f'size_XL')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2, button_3]], )
    return keyboard


def keyboard_size_hoodie1():
    logging.info("confirm_pay")
    button_1 = InlineKeyboardButton(text='M', callback_data=f'size1_M')
    button_2 = InlineKeyboardButton(text='L', callback_data=f'size1_L')
    button_3 = InlineKeyboardButton(text='XL', callback_data=f'size1_XL')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2, button_3]], )
    return keyboard


def keyboard_confirm_pay(merch_id):
    logging.info("confirm_pay_ton")
    button_1 = InlineKeyboardButton(text='Оплачено', callback_data=f'confirm_pay_for_{merch_id}')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data=f'cancel_pay_for_{merch_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard
