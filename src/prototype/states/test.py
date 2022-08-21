from aiogram.dispatcher.filters.state import StatesGroup, State


class registration(StatesGroup):
    client_fio = State()
    quest_fio = State()
    start_date = State()
    validity = State()


class accept(StatesGroup):
    user_id = State()


class reject(StatesGroup):
    user_id = State()
    