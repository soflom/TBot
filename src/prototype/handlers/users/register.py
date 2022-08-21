from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins_id
from filters import IsPrivate
from keyboards.default import kb_menu
from loader import dp

from states import registration, accept, reject
from utils.db_api import register_commands


@dp.message_handler(text='Отменить регистрацию', state=[registration.client_fio,
                                                        registration.quest_fio,
                                                        registration.start_date,
                                                        registration.validity])
async def quit_reg(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Регистрация отменена', reply_markup=kb_menu)


@dp.message_handler(IsPrivate(), Command('register'))
async def register_(message: types.Message):
    client_fio = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Ты начал регистрацию пропуска\nНапиши свои ФИО',
                         reply_markup=client_fio)
    await registration.client_fio.set()


@dp.message_handler(IsPrivate(), state=registration.client_fio)
async def get_client_fio(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(client_fio=answer)
    quest_fio = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Напиши ФИО гостя',
                         reply_markup=quest_fio)
    await registration.quest_fio.set()


@dp.message_handler(IsPrivate(), state=registration.quest_fio)
async def get_quest_fio(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(quest_fio=answer)
    start_date = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Напиши дату, когда пропуск должен начать действовать',
                         reply_markup=start_date)
    await registration.start_date.set()


@dp.message_handler(IsPrivate(), state=registration.start_date)
async def get_start_date(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(start_date=answer)
    validity = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить регистрацию')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer('Напиши нужный срок действия пропуска',
                         reply_markup=validity)
    await registration.validity.set()


@dp.message_handler(IsPrivate(), state=registration.validity)
async def get_validity(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(validity=answer)
    data = await state.get_data()
    name_of_client = data.get('client_fio')
    name_of_quest = data.get('quest_fio')
    start = data.get('start_date')
    end = data.get('validity')
    await register_commands.new_registration(user_id=message.from_user.id,
                                             client_fio=name_of_client,
                                             quest_fio=name_of_quest,
                                             start_date=start,
                                             validity=end,
                                             status='created')

    await message.answer(f'Регистрация пропуска успешно завершена\n'
                         f'Твои ФИО: {name_of_client}\n'
                         f'ФИО гостя: {name_of_quest}\n'
                         f'Дата начала пропуска: {start}\n'
                         f'Срок действия пропуска: {end}',
                         reply_markup=kb_menu)

    await state.finish()


@dp.message_handler(IsPrivate(), text='/admin', user_id=admins_id)
async def get_reg(message: types.Message):
    reg = await register_commands.select_registration()
    ikb = InlineKeyboardMarkup(row_width=1,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text='Accept',
                                                            callback_data='Accept'),
                                       InlineKeyboardButton(text='Reject',
                                                            callback_data='Reject')
                                   ]
                               ])
    await message.answer(f'Дата создания: {reg.created_at}\n'
                         f'id: {reg.user_id}\n'
                         f'name_of_client: {reg.client_fio}\n'
                         f'name_of_quest: {reg.quest_fio}\n'
                         f'start: {reg.start_date}\n'
                         f'end: {reg.validity}\n',
                         reply_markup=ikb)


@dp.callback_query_handler(text='Accept')
async def accept_reg(call: types.CallbackQuery):
    await call.message.answer(f'Введите айди для подтверждения')
    await accept.user_id.set()


@dp.message_handler(state=accept.user_id)
async def accept_reg(message: types.Message, state: FSMContext):
    await register_commands.accept_registration(message.from_user.id)
    await message.answer(f'Айди подтвержден. Заявка одобрена')
    await state.finish()


@dp.callback_query_handler(text='Reject')
async def reject_reg(call: types.CallbackQuery):
    await call.message.answer(f'Введите айди для подтверждения')
    await reject.user_id.set()


@dp.message_handler(state=reject.user_id)
async def reject_reg(message: types.Message, state: FSMContext):
    await register_commands.reject_registration(message.from_user.id)
    await message.answer(f'Айди подтвержден. Заявка отклонена')
    await state.finish()
