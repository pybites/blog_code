#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date

from mail import email, PYBITES_EMAIL

ERROR_MSG = 'expected result for input var {} = {}'
DAYS_IN_YEAR = 365
SPECIAL_DAY_OFFSETS = (100, DAYS_IN_YEAR)
TODAY = date.today()
PYBITES_START = date(year=2016, month=12, day=19)
AGE_DAYS = (TODAY - PYBITES_START).days
PYBITES = 'PyBites'

def today_is_special_day(age=None):
    if age is None:
        age = AGE_DAYS
    return any(map(lambda x: age % x == 0, SPECIAL_DAY_OFFSETS))


def days_till_bday(age=None):
    if age is None:
        age = AGE_DAYS
    return min(map(lambda x: x - age % x, SPECIAL_DAY_OFFSETS))


if __name__ == "__main__":
    def test_today_is_special_day():
        test_days = (1, 50, 100, 101, 200, 305, 365, 400, 499, 730, 800, 850)
        test_outcomes = (False, False, True, False, True, False,
                        True, True, False, True, True, False)
        for age, outcome in zip(test_days, test_outcomes):
            assert today_is_special_day(age) == outcome, ERROR_MSG.format(age, outcome)

    def test_days_till_bday():
        test_days = (1, 50, 100, 101, 200, 305, 365, 400, 499, 730, 800, 850)
        test_outcomes = (99, 50, 100, 99, 100, 60, 35, 100, 1, 70, 100, 50)
        for age, outcome in zip(test_days, test_outcomes):
            assert days_till_bday(age) == outcome, ERROR_MSG.format(age, outcome)

    test_today_is_special_day()
    test_days_till_bday()

    print('{} is {} days old'.format(PYBITES, AGE_DAYS))
    print('Does {} have a birthday today?'.format(PYBITES))

    if today_is_special_day():
        whatday = 'birthday' if AGE_DAYS % DAYS_IN_YEAR == 0 else 'celebration day'
        subject = 'Happy {}!'.format(whatday)
        message = '{} exists {} days today, go celebrate!'.format(PYBITES, AGE_DAYS)
        email(PYBITES_EMAIL, subject, message)
        print('Yes!')
    else:
        print('No ... days till next birtday: {}'.format(days_till_bday()))
