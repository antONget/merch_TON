from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import logging


def keyboards_main() -> ReplyKeyboardMarkup:
    logging.info("keyboards_main")
    button_1 = KeyboardButton(text='Поддержка')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                   resize_keyboard=True)
    return keyboard


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
    button_2 = InlineKeyboardButton(text='Отмена', callback_data=f'order_cancel_{id_order}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard

def keyboard_confirm_pay(merch_id):
    logging.info("confirm_pay_ton")
    button_1 = InlineKeyboardButton(text='Оплачено', callback_data=f'confirm_pay_for_{merch_id}')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data=f'cancel_pay_for_{merch_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard
