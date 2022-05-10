from datetime import datetime


class PaystatMonthlyReport:
    def __init__(self, date: datetime, age: str, gender: str, amount: float):
        self.date: datetime = date.isoformat()
        self.age: str = age
        self.gender: str = gender
        self.amount: float = amount
