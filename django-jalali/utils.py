import re
import datetime
from typing import Tuple, Union

class DateParser:
    _DATE_PATTERN = re.compile(r'(\d{4})\D(\d{1,2})\D(\d{1,2})')

    @staticmethod
    def parse(date_input: Union[str, Tuple, datetime.date], calendar: str) -> Tuple[int, int, int]:
        if isinstance(date_input, str):
            return DateParser._parse_string(date_input)
        if isinstance(date_input, tuple):
            return DateParser._parse_tuple(date_input)
        if calendar.lower() == "gregorian" and isinstance(date_input, datetime.date):
            return date_input.year, date_input.month, date_input.day
        raise ValueError("Invalid Input Type")

    @staticmethod
    def _parse_string(date_str: str) -> Tuple[int, int, int]:
        match = DateParser._DATE_PATTERN.fullmatch(date_str)
        if not match:
            raise ValueError("Invalid Input String")
        return tuple(map(int, match.groups()))

    @staticmethod
    def _parse_tuple(date_tuple: Tuple) -> Tuple[int, int, int]:
        if len(date_tuple) != 3:
            raise ValueError("Invalid Input Tuple")
        return tuple(map(int, date_tuple))


class PersianUtils:
    _PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

    @staticmethod
    def convert_numbers(text: str) -> str:
        return text.translate(PersianUtils._PERSIAN_DIGITS)
