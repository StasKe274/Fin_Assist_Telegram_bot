import logging
from aiogram import Bot, Dispatcher, executor, types
from env_variables import api_token
import expenses
import db

# api token telegramm
API_TOKEN = api_token

# logging config
logging.basicConfig(filename='bot.log', filemode='w')

#initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # Welcome message /start, /help
    await message.answer(
            'Финансовый помощник.\n\n'
            'Добавить расход: просто введите расход\n'
            'Статистика на сегодня: /today\n'
            'Статистика за месяц: /month\n'
            'Последние расходы: /last\n'
            'Установить лимит: /set_limit\n')


@dp.message_handler(commands=['today'])
async def today_statistic(message: types.Message):
    # Return statistic for today
    await message.answer('Вернулась статистика на сегодня')


@dp.message_handler(commands=['month'])
async def month_statistic(message: types.Message):
    # Return expenses statistic for month
    await message.answer('Вернулась статистика за месяц')


@dp.message_handler(commands=['last'])
async def last_expenses(message: types.Message):
    # Return last expenses for today
    answer = 'Последние расходы:\n\n' + expenses.last_expenses()
    await message.answer(answer)

 
@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    # Delete expense by name
    raw_message = message.text[4:]
    try:
        expenses.delete_expense(raw_message)
        await message.answer('Удалил по идентификатору')
    except Exception as ex:
        await message.answer('Удалить не получилось, попробуйте снова')
        logging.error(ex)


@dp.message_handler(commands=['set_limit'])
async def set_limit(message: types.Message):
    # set a limit for day
    try:
        expenses.set_limit(message.text)
        await message.answer('Лимит установлен')
    except Exception as ex:
        await message.answer('Не удалось установить лимит...')
        logging.error(ex)


@dp.message_handler()
async def add_expense(message: types.Message):
    # add new expens in db
    try:
        expenses.add_new_expense(message.text)
        try:
            residue = expenses.count_residue_from_limit()
            answer = f'Запись добавлена.\n{residue}'
        except:
            answer = 'Запись добавлена.'
        await message.answer(answer)
    except Exception as ex:
        await message.answer('Ошибка')
        logging.error(ex)


if __name__ == '__main__':
    db.db_init()
    executor.start_polling(dp, skip_updates=True)


