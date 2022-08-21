from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Получить пропуск', callback_data='Создать'),
                                    ],
                                    [
                                        InlineKeyboardButton(text='alert', callback_data='alert'),
                                        InlineKeyboardButton(text='Сюрприз', url='https://vk.com/ilikesomeham')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Скрыть нижние кнопки', callback_data='Кнопки2')
                                    ]
                                ])
