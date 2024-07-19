from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboard_refer():
    logging.info("keyboard_refer")
    button_1 = InlineKeyboardButton(text='Получить реферальную ссылку',
                                    callback_data='refer')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]])
    return keyboard
