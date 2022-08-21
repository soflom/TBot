from aiogram import types
from loader import dp


@dp.message_handler(text='Го доту')
async def buttons_test(message: types.Message):
    await message.answer(f'Ааххахахахахаххахахахахахах нет')
