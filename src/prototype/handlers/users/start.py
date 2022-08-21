from aiogram import types
from loader import dp

from filters import IsPrivate
from utils.misc import rate_limit


@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    photo_file_id = 'AgACAgIAAxkBAAIC8GL_5t6QT0Hnwx1Agx4Bq2Hl6kY9AALgvTEbFRUAAUiY_KTpwx3GZAEAAwIAA3gAAykE'
    await dp.bot.send_photo(chat_id=message.from_user.id, photo=photo_file_id, caption=f'Привет, {message.from_user.full_name}!\nТебя приветствует Passbot21! \n'
                         f'Твой айди: {message.from_user.id}')
