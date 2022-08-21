from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu2 = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Получить пропуск', callback_data='Создать'),
                                    ]
                                ])
