import calendar
import datetime


def author_directory_path(instance, filename):
    return f'uploads/author_{instance.author.id}/{filename}'


def add_months_to_date(date, months_count) -> datetime.date:
    month = date.month - 1 + months_count
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)