from sqlalchemy import Column, Integer, String, Date, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///fin_assist.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


db = declarative_base()
class Budget(db):
    __tablename__ = 'buget'
    id = Column(Integer, primary_key=True)
    limit = Column(Integer)


    def __init__(self, limit):
        self.limit = limit


class Expense(db):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    expense = Column(Integer)
    category = Column(String)


    def __init__(self, date, time, expense, category):
        self.date = date
        self.time = time
        self.expense = expense
        self.category = category


def db_init() -> None:
    db.metadata.create_all(engine)


def insert_expense(date, time, expense: int, category: str) -> None:
    insert_data = Expense(date, time, expense, category)
    session.add(insert_data)
    session.commit()


def insert_limit(limit: int) -> None:
    insert_data = Budget(limit)
    session.add(insert_data)
    session.commit()


def get_limit():
    # actual_limit = session.query(Budget).filter(Budget.id==3).first()
    get_limit = session.query(Budget).order_by(Budget.id.desc()).first()
    actual_limit = get_limit.limit
    return actual_limit


def get_last_expenses(date):
    data_for_answer = []
    data_for_residue_count = []
    last_expenses = session.query(Expense).filter(Expense.date==date).all()
    counter = 1
    for expense in last_expenses:
        append_data = str(counter) + ') ' \
                + str(expense.expense) + ' ' \
                + str(expense.category) + '\n'
        data_for_answer.append(append_data)
        data_for_residue_count.append(expense.expense)
        counter+=1
    sum_of_expenses = sum(data_for_residue_count)
    return [data_for_answer, sum_of_expenses]


def delete(expense: int, category: str) -> None:
    delete_data = _find(expense, category)
    session.delete(delete_data)
    session.commit()


def _find(expense: int, category: str):
    expense = session.query(Expense) \
            .filter(Expense.expense==expense) \
            .filter(Expense.category==category).first()
    return expense
