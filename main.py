import asyncio
from aiogram import Bot, Dispatcher, types, executor
from personal import *
import yaml
from db_sqllite import *


with open('config.yaml') as f:
    config = yaml.safe_load(f)

TOKEN = config['telegram_token']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db_object = UserBD()
db_object.get_users_telegram_ids()


def set_user(func):
    async def wrapper(message: types.Message):
        active_user = db_object.active_users
        if message.from_user.id not in active_user:
            return await message.reply(f'I don`t know who are u, u should use /start command', reply=False)
            # active_user[message.from_user.id] = PersonalCcalCalculator(message.from_user.id,
            #                                                            message.from_user.username)
        user = active_user[message.from_user.id]
        return await func(message, user)
    return wrapper


@dp.message_handler(commands={'start'})
async def start_handler(message: types.Message):
    active_user = db_object.active_users
    if message.from_user.id in active_user:
        await message.reply(f'Hello u already in db', reply=False)
        return


@dp.message_handler(commands={'food'})
@set_user
async def get_food_list(message: types.Message, user: PersonalCcalCalculator):
    food_formatted_str = '\nП/П. НАЗВАНИЕ: ККАЛ'
    for num, food in enumerate(user.food):
        temp_str = f"\n{num}. {food['label']}: {food['ccal']}"
        food_formatted_str += temp_str
    await message.answer(f"```{food_formatted_str}```", parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(commands={'clear'})
@set_user
async def clear(message: types.Message, user: PersonalCcalCalculator):
    del user.food
    await message.answer(f'Список с продуктами очищен')


@dp.message_handler(commands={'del'})
@set_user
async def clear(message: types.Message, user: PersonalCcalCalculator):
    try:
        command, number = message.text.split()
        user.food = int(number)
        await message.answer(f'Удалено')
    except (ValueError, IndexError):
        await message.answer(f'Неверные данные')


@dp.message_handler()
@set_user
async def add_ccal(message: types.Message, user: PersonalCcalCalculator):
    try:
        _food, ccal = user.how_much_ccal(message.text)
        user.food = _food, ccal
        await message.answer(f'{user.ccal_left}')
    except (ValueError, IndexError):
        await message.answer(f'Неверные данные, попробуйте еще раз: НАЗВАНИЕ КкалНаСтоГрамм Грамм')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)