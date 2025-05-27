from django.db import models
from datetime import date, datetime, time
from .conversion import PersianDate, GregorianDate

class JalaliDateField(models.DateField):
    description = "Jalali date stored as Gregorian date internally"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        g_date = GregorianDate(value.year, value.month, value.day)
        return f"{g_date.persian_year:04d}/{g_date.persian_month:02d}/{g_date.persian_day:02d}"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, date):
            g_date = GregorianDate(value.year, value.month, value.day)
            return f"{g_date.persian_year:04d}/{g_date.persian_month:02d}/{g_date.persian_day:02d}"
        if isinstance(value, str):
            value = value.replace('-', '/')
            p_date = PersianDate(value)
            y, m, d = p_date.get_gregorian_tuple()
            return date(y, m, d)
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            p_date = PersianDate(value.replace('-', '/'))
            y, m, d = p_date.get_gregorian_tuple()
            return date(y, m, d)
        if isinstance(value, date):
            return value
        raise ValueError(f"Invalid type for JalaliDateField: {type(value)}")


class JalaliDateTimeField(models.DateTimeField):
    description = "Jalali datetime stored as Gregorian datetime internally"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        g_date = GregorianDate(value.year, value.month, value.day)
        jalali_date_str = f"{g_date.persian_year:04d}/{g_date.persian_month:02d}/{g_date.persian_day:02d}"
        return f"{jalali_date_str} {value.hour:02d}:{value.minute:02d}:{value.second:02d}"

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime):
            g_date = GregorianDate(value.year, value.month, value.day)
            jalali_date_str = f"{g_date.persian_year:04d}/{g_date.persian_month:02d}/{g_date.persian_day:02d}"
            return f"{jalali_date_str} {value.hour:02d}:{value.minute:02d}:{value.second:02d}"
        if isinstance(value, str):
            date_part, time_part = value.strip().split(" ")
            date_part = date_part.replace("-", "/")
            p_date = PersianDate(date_part)
            y, m, d = p_date.get_gregorian_tuple()
            h, mi, s = map(int, time_part.split(":"))
            return datetime(y, m, d, h, mi, s)
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            date_part, time_part = value.strip().split(" ")
            date_part = date_part.replace("-", "/")
            p_date = PersianDate(date_part)
            y, m, d = p_date.get_gregorian_tuple()
            h, mi, s = map(int, time_part.split(":"))
            return datetime(y, m, d, h, mi, s)
        if isinstance(value, datetime):
            return value
        raise ValueError(f"Invalid type for JalaliDateTimeField: {type(value)}")


class JalaliTimeField(models.TimeField):
    description = "Time field with Jalali-compatible input/output (time only)"

    def from_db_value(self, value, expression, connection):
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, time):
            return value
        if isinstance(value, str):
            try:
                h, m, s = map(int, value.split(":"))
                return time(h, m, s)
            except Exception:
                raise ValueError(f"Invalid time format: {value}")
        return value
