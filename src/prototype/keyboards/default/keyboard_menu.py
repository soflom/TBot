from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Инлайн меню'),
        ],
        [
            KeyboardButton(text='Выйти'),
            KeyboardButton(text='Го доту')
        ],
    ],
    resize_keyboard=True
)