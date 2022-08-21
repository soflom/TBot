from aiogram import types

from keyboards.default import kb_test
from loader import dp


@dp.message_handler(text='Выйти')
async def test(message: types.Message):
    await message.answer(f'Меню скрыто', reply_markup=kb_test)
