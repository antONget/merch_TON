from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_add_merch():
    logging.info("keyboard_create_merch")
    button_1 = InlineKeyboardButton(text='hoodie 👘',
                                    callback_data='add_merch_hoodie')
    button_2 = InlineKeyboardButton(text='cup ☕️',
                                    callback_data='add_merch_cup')
    button_3 = InlineKeyboardButton(text='flag 🚩',
                                    callback_data='add_merch_flag')
    button_4 = InlineKeyboardButton(text='anon merch 🎱',
                                    callback_data='add_merch_anon')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],)
    return keyboard


def keyboard_add_merch_anon():
    logging.info("keyboard_create_merch")
    button_1 = InlineKeyboardButton(text='hoodie 👘',
                                    callback_data='anonadd_merch_hoodie')
    button_2 = InlineKeyboardButton(text='cup ☕️',
                                    callback_data='anonadd_merch_cup')
    button_3 = InlineKeyboardButton(text='flag 🚩',
                                    callback_data='anonadd_merch_flag')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard