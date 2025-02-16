import datetime
from .utils import DateParser

class GregorianDate:
    def __init__(self, *date):
        if len(date) == 1:
            year, month, day = DateParser.parse(date[0], "gregorian")
        elif len(date) == 3:
            year, month, day = map(int, date)
        else:
            raise ValueError("Invalid Input")
        
        try:
            datetime.datetime(year, month, day)
        except Exception:
            raise ValueError("Invalid Date")
        
        self.gregorian_year = year
        self.gregorian_month = month
        self.gregorian_day = day
        
        self._convert_to_persian()
    
    def _convert_to_persian(self):
        d_4 = self.gregorian_year % 4
        g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        doy_g = g_a[self.gregorian_month] + self.gregorian_day
        if d_4 == 0 and self.gregorian_month > 2:
            doy_g += 1
        d_33 = int(((self.gregorian_year - 16) % 132) * 0.0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((self.gregorian_year - 10) / 63) == 30:
            a -= 1
            b += 1
        if doy_g > b:
            jy = self.gregorian_year - 621
            doy_j = doy_g - b
        else:
            jy = self.gregorian_year - 622
            doy_j = doy_g + a
        if doy_j < 187:
            jm = int((doy_j - 1) / 31)
            jd = doy_j - (31 * jm)
            jm += 1
        else:
            jm = int((doy_j - 187) / 30)
            jd = doy_j - 186 - (jm * 30)
            jm += 7
        self.persian_year = jy
        self.persian_month = jm
        self.persian_day = jd
    
    def to_persian(self):
        from .conversion import PersianDate
        return PersianDate(self.persian_year, self.persian_month, self.persian_day)
    
    def get_persian_tuple(self):
        return (self.persian_year, self.persian_month, self.persian_day)
    
    def get_persian_string(self, date_format="{}-{}-{}"):
        return date_format.format(self.persian_year, self.persian_month, self.persian_day)


class PersianDate:
    def __init__(self, *date):
        if len(date) == 1:
            from .utils import DateParser
            year, month, day = DateParser.parse(date[0], "persian")
        elif len(date) == 3:
            year, month, day = map(int, date)
        else:
            raise ValueError("Invalid Input")
        
        if year < 1 or month < 1 or month > 12 or day < 1 or day > 31 or (month > 6 and day == 31):
            raise ValueError("Incorrect Date")
        
        self.persian_year = year
        self.persian_month = month
        self.persian_day = day
        
        self._convert_to_gregorian()
    
    def _convert_to_gregorian(self):
        d_4 = (self.persian_year + 1) % 4
        if self.persian_month < 7:
            doy_j = ((self.persian_month - 1) * 31) + self.persian_day
        else:
            doy_j = ((self.persian_month - 7) * 30) + self.persian_day + 186
        d_33 = int(((self.persian_year - 55) % 132) * 0.0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((self.persian_year - 19) / 63) == 20:
            a -= 1
            b += 1
        if doy_j <= a:
            gy = self.persian_year + 621
            gd = doy_j + b
        else:
            gy = self.persian_year + 622
            gd = doy_j - a
        gregorian_month = 0
        for gm, v in enumerate([0, 31, 29 if (gy % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gd <= v:
                gregorian_month = gm
                break
            gd -= v
        self.gregorian_year = gy
        self.gregorian_month = gregorian_month
        self.gregorian_day = gd
    
    def to_gregorian(self):
        from .conversion import GregorianDate
        return GregorianDate(self.gregorian_year, self.gregorian_month, self.gregorian_day)
    
    def get_gregorian_tuple(self):
        return (self.gregorian_year, self.gregorian_month, self.gregorian_day)
    
    def get_gregorian_string(self, date_format="{}-{}-{}"):
        return date_format.format(self.gregorian_year, self.gregorian_month, self.gregorian_day)
    
    def to_gregorian_datetime(self):
        return datetime.date(self.gregorian_year, self.gregorian_month, self.gregorian_day)
