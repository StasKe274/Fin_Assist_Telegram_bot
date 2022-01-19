"""Work with expenses, main logic, append, delete expenses, analitics"""
import exceptions
from typing import NamedTuple
import db
import datetime
from categories import CATEGORIES


class Message(NamedTuple):
    # Structure of message with expense
    expense: int
    category: str


def add_new_expense(message: str) -> None:
    # Add new expense in database
    date = datetime.date.today()
    time = datetime.datetime.now().time()
    expense = _parse_message(message).expense
    category = str(_get_category(_parse_message(message).category))
    db.insert_expense(date, time, expense, category)


def set_limit(message: str) -> None:
    # Set a limit for a day
    try:
        raw_message = list(message.strip().split(' '))
        limit = int(raw_message[1])
        db.insert_limit(limit)
    except Exception:
        raise exceptions.NotCorrectMessage('Не понял, попробуйте снова')


def delete_expense(message: str) -> None:
    # Delete expense by id from database
    expense = _parse_message(message).expense
    category = str(_get_category(_parse_message(message).category))
    db.delete(expense, category)


def last_expenses():
    # Retern list with last expenses for today
    date = datetime.date.today()
    last_expenses = db.get_last_expenses(date)
    if len(last_expenses[0]) == 0:
        return 'Расходов пока нет!'
    else:
        res = ''
        for expense in last_expenses[0]:
            res+=expense
        return res


def get_today_statistic():
    # Return statistic for today
    pass


def get_month_statistic():
    # Return month statistic
    pass


def count_residue_from_limit():
    # Residue for day
    limit = db.get_limit()
    date = datetime.date.today()
    expenses_per_day = db.get_last_expenses(date)[1]
    residue = limit - expenses_per_day
    if residue >= 0:
        data = [expenses_per_day, limit, residue]
        answer = f'Потрачено {str(data[0])} из {str(data[1])}\nОстаток: {str(data[2])}'
        return answer
    elif residue < 0:
        residue = -(residue)
        data = [expenses_per_day, limit, residue]
        answer = f'Потрачено {str(data[0])} из {str(data[1])}\nПерерасход: {str(data[2])}'
        return answer


def _parse_message(message: str):
    # Parse message for database
    try:
        insert_data = list(message.strip().split(' '))
        expense = int(insert_data[0])
        category = insert_data[1]
        print(insert_data)
        return Message(expense=expense, category=category)
    except Exception:
        raise exceptions.NotCorrectMessage('Не могу понять сообщение, попробуйте еше раз')


def _get_category(category: str):
    for aliases in CATEGORIES:
        if category in aliases:
            return str(aliases[0])
        else:
            continue
    else:
        category = 'other' 
        return category


    

