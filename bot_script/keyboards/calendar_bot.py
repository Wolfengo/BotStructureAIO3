import requests
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
import asyncio
import datetime
import json

from bot_script.config import timeZone, localization


async def calendar_builder(language: str = localization, callback_type: str = 'client', year_in=None, month_in=None):
    with open('keyboards/localization.json', 'r') as file:
        months = json.load(file)
    months = months['calendar']
    current_date = datetime.datetime.utcnow() + datetime.timedelta(hours=timeZone)
    year = year_in if year_in else current_date.year
    month = month_in if month_in else current_date.month
    cal = calendar.Calendar()
    month_name = months[language]["months"][str(month)] if language in months else months[localization]["months"][str(month)]
    month_days = cal.monthdays2calendar(year, month)

    keyboard = InlineKeyboardBuilder()

    left = InlineKeyboardButton(text='<<<', callback_data=f'left_calendar_{callback_type}')
    right = InlineKeyboardButton(text='>>>', callback_data=f'right_calendar_{callback_type}')
    data_calendar = InlineKeyboardButton(text=f'{month_name} {year}', callback_data=f'ignore')
    keyboard.row(left, data_calendar, right)

    days = months[language]['days'] if language in months else months[localization]["days"]
    row = []
    for day_num in days:
        row.append(InlineKeyboardButton(text=days[day_num], callback_data='ignore'))
    keyboard.row(*row)

    for week in month_days:
        row = []
        for day, _ in week:
            row.append(InlineKeyboardButton(text=' ' if day == 0 else str(day),
                                            callback_data='ignore' if day == 0 else
                                            f'{month}_{str(day)}_{callback_type}'))
        keyboard.row(*row)

    return keyboard.as_markup()


if __name__ == '__main__':
    asyncio.run(calendar_builder("ru"))
