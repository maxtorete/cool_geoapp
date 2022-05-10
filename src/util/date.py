from datetime import datetime


def get_date_frame(date_from: datetime, date_to: datetime):
    if date_from is None or date_to is None:
        raise ValueError

    date_from = datetime.fromisoformat(date_from)
    date_to = datetime.fromisoformat(date_to)
    if date_from > date_to:
        raise ValueError

    return [date_from, date_to]
