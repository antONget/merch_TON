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
    button_5 = InlineKeyboardButton(text='T-shirt 👕👚',
                                    callback_data='add_merch_tshirt')
    button_6 = InlineKeyboardButton(text='BOXES 🎁',
                                    callback_data='add_merch_boxes')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5], [button_6]],)
    return keyboard


def keyboard_add_merch_anon():
    logging.info("keyboard_create_merch")
    button_1 = InlineKeyboardButton(text='hoodie 👘',
                                    callback_data='anonadd_merch_hoodie')
    button_2 = InlineKeyboardButton(text='cup ☕️',
                                    callback_data='anonadd_merch_cup')
    button_3 = InlineKeyboardButton(text='flag 🚩',
                                    callback_data='anonadd_merch_flag')
    button_4 = InlineKeyboardButton(text='T-shirt 👕👚',
                                    callback_data='anonadd_merch_tshirt')
    button_5 = InlineKeyboardButton(text='BOXES 🎁',
                                    callback_data='anonadd_merch_boxes')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5]],)
    return keyboard