from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_card_merch_anon(list_merch: list, block: int):
    logging.info("keyboards_card_merch_anon")
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    text = f'Купить'
    button = f'anonbay_{list_merch[block].id_merch}'
    buttons.append(InlineKeyboardButton(
        text=text,
        callback_data=button))
    button_back = InlineKeyboardButton(text='<<',
                                       callback_data=f'anonback_{str(block)}')
    button_next = InlineKeyboardButton(text='>>',
                                       callback_data=f'anonforward_{str(block)}')
    kb_builder.row(*buttons, width=1)
    kb_builder.row(button_back, button_next)
    return kb_builder.as_markup()


def keyboard_size_hoodie_anon():
    logging.info("keyboard_size_hoodie_anon")
    button_1 = InlineKeyboardButton(text='L', callback_data=f'anonsize_L')
    button_2 = InlineKeyboardButton(text='XL', callback_data=f'anonsize_XL')
    button_3 = InlineKeyboardButton(text='XXL', callback_data=f'anonsize_XXL')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2, button_3]], )
    return keyboard


def keyboard_confirm_pay_anon(merch_id):
    logging.info("keyboard_confirm_pay_anon")
    button_1 = InlineKeyboardButton(text='Оплачено', callback_data=f'anonconfirm_pay_for_{merch_id}')
    button_2 = InlineKeyboardButton(text='Отмена', callback_data=f'anoncancel_pay_for_{merch_id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]], )
    return keyboard
