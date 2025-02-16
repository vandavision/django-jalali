import datetime
from conversion import GregorianDate, PersianDate
from formatters import JalaliDateTime

if __name__ == "__main__":
    g_date = GregorianDate("2025-02-16")
    print("Gregorian -> Persian (Tuple):", g_date.get_persian_tuple())
    print("Gregorian -> Persian (String):", g_date.get_persian_string())
    
    p_date = PersianDate("1403/12/27")
    print("Persian -> Gregorian (Tuple):", p_date.get_gregorian_tuple())
    print("Persian -> Gregorian (String):", p_date.get_gregorian_string())
    
    now = datetime.datetime.now()
    jdt = JalaliDateTime(now)
    print("Formatted Full:", jdt.format_full())
    print("Formatted Numeric:", jdt.format_numeric())
    print("Formatted Date Only:", jdt.format_date_only())
