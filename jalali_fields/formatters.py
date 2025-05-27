import datetime
from django.utils import timezone
from .conversion import PersianDate
from .utils import PersianUtils

class PersianDateFormatter:
    JMONTHS = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد",
        "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    JDAYS = [
        "شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"
    ]
    
    @staticmethod
    def format_full(persian_date: PersianDate, dt: datetime.datetime) -> str:
        day_name = PersianDateFormatter.JDAYS[dt.weekday()]
        month_name = PersianDateFormatter.JMONTHS[persian_date.persian_month - 1]
        output = "{}، {} {} {}، ساعت {}:{}".format(
            day_name,
            persian_date.persian_day,
            month_name,
            persian_date.persian_year,
            dt.hour,
            dt.minute,
        )
        return PersianUtils.convert_numbers(output)
    
    @staticmethod
    def format_numeric(persian_date: PersianDate, dt: datetime.datetime) -> str:
        output = "{}/{}/{}، ساعت {}:{}".format(
            persian_date.persian_year,
            persian_date.persian_month,
            persian_date.persian_day,
            dt.hour,
            dt.minute,
        )
        return PersianUtils.convert_numbers(output)

    @staticmethod
    def format_date_only(persian_date: PersianDate) -> str:
        output = "{}-{}-{}".format(persian_date.persian_year, persian_date.persian_month, persian_date.persian_day)
        return PersianUtils.convert_numbers(output)


class JalaliDateTime:
    def __init__(self, dt: datetime.datetime):
        self.dt = timezone.localtime(dt)
        from .conversion import GregorianDate
        gregorian_date = GregorianDate(self.dt.year, self.dt.month, self.dt.day)
        self.persian_date = PersianDate(gregorian_date.get_persian_tuple())
    
    def format_full(self) -> str:
        return PersianDateFormatter.format_full(self.persian_date, self.dt)
    
    def format_numeric(self) -> str:
        return PersianDateFormatter.format_numeric(self.persian_date, self.dt)

    def format_date_only(self) -> str:
        return PersianDateFormatter.format_date_only(self.persian_date)