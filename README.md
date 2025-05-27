# Django Jalali DateTime Fields

A comprehensive Django package providing custom model fields to seamlessly work with Jalali (Persian) dates and times. This package handles conversion between Jalali (Persian) calendar dates and Gregorian calendar dates internally, enabling developers to store Gregorian dates in the database while working with Jalali dates in the application layer.

---

## Features

- **JalaliDateField**: Custom `DateField` that accepts and outputs Jalali dates, stores internally as Gregorian dates.
- **JalaliDateTimeField**: Custom `DateTimeField` that supports Jalali date and time strings, storing internally as Gregorian datetimes.
- **JalaliTimeField**: Custom `TimeField` that handles time values compatible with Jalali date usage.
- Transparent conversion both ways between Jalali and Gregorian.
- Persian date formatting utilities for full textual or numeric Jalali date/time representation.
- Robust parsing and validation for date/time strings and Python date/time objects.
- Persian digit conversion for UI-friendly Jalali date strings.

---

## Installation

Copy the package files into your Django project or integrate as a module.

> **Note:** This package relies on custom date conversion logic provided by the `conversion.py`, `formatters.py`, and `utils.py` modules included here.

---

## Usage

### Model Fields

Use the custom Jalali fields in your Django models instead of the standard date/time fields:

```python
from django.db import models
from jalali_fields import JalaliDateField, JalaliDateTimeField, JalaliTimeField

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date = JalaliDateField()
    start_datetime = JalaliDateTimeField()
    start_time = JalaliTimeField()