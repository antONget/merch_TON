from aiogram import Bot

from aiogram.types import Message, CallbackQuery, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner,\
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Filter
from config_data.config import Config, load_config

config: Config = load_config()


class ChannelProtect(Filter):
    async def __call__(self, message: Message, bot: Bot):
        u_status = await bot.get_chat_member(chat_id=config.tg_bot.channel_name, user_id=message.from_user.id)
        if isinstance(u_status, ChatMemberMember) or isinstance(u_status, ChatMemberAdministrator) \
                or isinstance(u_status, ChatMemberOwner):
            return True
        button_1 = InlineKeyboardButton(text='Я подписался', callback_data='subscription')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
        if isinstance(message, CallbackQuery):
            await message.answer()

            await message.message.answer(text=f'Чтобы получать вознаграждения за приглашенных пользователей, а самому'
                                              f' найти вакансию своей мечты подпишись на канал '
                                              f'<a href="{config.tg_bot.channel_name}">'
                                              f'{config.tg_bot.channel_name}</a>',
                                         reply_markup=keyboard,
                                         parse_mode='html')
        else:
            await message.answer(text=f'Чтобы получать вознаграждения за приглашенных пользователей, а самому найти'
                                      f' вакансию своей мечты подпишись на канал '
                                      f'<a href="{config.tg_bot.channel_name}">{config.tg_bot.channel_name}</a>',
                                 reply_markup=keyboard,
                                 parse_mode='html')
        return False