from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_main() -> ReplyKeyboardMarkup:
    logging.info("keyboards_main")
    button_1 = KeyboardButton(text='hoodie')
    button_2 = KeyboardButton(text='cup')
    button_3 = KeyboardButton(text='create your merch')
    button_4 = KeyboardButton(text='Поддержка')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3], [button_4]],
                                   resize_keyboard=True)
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

# def keyboards_card_merch(list_merch: list, back: int, forward: int, count: int):
#     logging.info("keyboards_card_merch")
#     # проверка чтобы не ушли в минус
#     if back < 0:
#         back = 0
#         forward = 2
#     # считаем сколько всего блоков по заданному количество элементов в блоке
#     count_users = len(list_merch)
#     whole = count_users // count
#     remains = count_users % count
#     max_forward = whole + 1
#     # если есть остаток, то увеличиваем количество блоков на один, чтобы показать остаток
#     if remains:
#         max_forward = whole + 2
#     if forward > max_forward:
#         forward = max_forward
#         back = forward - 2
#     kb_builder = InlineKeyboardBuilder()
#     buttons = []
#
#     for merch in list_merch[back*count:(forward-1)*count]:
#
#         text = f'Купить'
#         button = f'bay_{merch.id_merch}'
#         buttons.append(InlineKeyboardButton(
#             text=text,
#             callback_data=button))
#     button_back = InlineKeyboardButton(text='<<',
#                                        callback_data=f'back_{str(back)}')
#     button_next = InlineKeyboardButton(text='>>',
#                                        callback_data=f'forward_{str(forward)}')
#     kb_builder.row(*buttons, width=1)
#     kb_builder.row(button_back, button_next)
#     return kb_builder.as_markup()


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
