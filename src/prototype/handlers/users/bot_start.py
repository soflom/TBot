from aiogram import types
from loader import dp

from filters import IsPrivate
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer(f'Привет, {user.first_name}\n'
                                 f'Ты уже зарегистрирован')
        elif user.status == 'baned':
            await message.answer('Ты забанен')
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                status='active')
        await message.answer('Ты зарегистрирован')


@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: types.Message):
    await commands.update_status(user_id=message.from_user.id, status='baned')
    await message.answer('Забанен')


@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), text='/unban')
async def get_unban(message: types.Message):
    await commands.update_status(user_id=message.from_user.id, status='active')
    await message.answer('Разбанен')


@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), text='/profile')
async def profile(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.answer(f'Aйди - {user.user_id}\n'
                         f'Имя - {user.first_name}\n'
                         f'Фамилия - {user.last_name}\n'
                         f'username - {user.username}\n'
                         f'status - {user.status}\n')



