import datetime
import unittest

from todo.utils import date_to_relative


class TestDateToRelative(unittest.TestCase):
    def test_should_return_today(self):
        today = datetime.date.today()
        result = date_to_relative(today)
        self.assertEqual(result, "today")

    def test_should_return_tomorrow(self):
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        result = date_to_relative(tomorrow)
        self.assertEqual(result, "tomorrow")

    def test_should_return_yesterday(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        result = date_to_relative(yesterday)
        self.assertEqual(result, "yesterday")

    def test_should_return_weekdays_after_tomorrow(self):
        weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        six_days_after = datetime.date.today() + datetime.timedelta(days=6)
        result = date_to_relative(six_days_after)
        expected = weekdays[six_days_after.weekday()]
        self.assertEqual(result, expected)

    def test_should_return_absolute_date_after_a_week(self):
        after7days = datetime.date.today() + datetime.timedelta(days=7)
        result = date_to_relative(after7days)
        self.assertEqual(result, after7days.isoformat())
