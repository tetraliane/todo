import datetime
import unittest
from todo.parser import *


class TestDateParser(unittest.TestCase):
    def test_should_accept_absolute_date(self):
        result = parse_date("2023-05-30")
        self.assertEqual(result, datetime.date(2023, 5, 30))
        result = parse_date("2023/05/30")
        self.assertEqual(result, datetime.date(2023, 5, 30))
        result = parse_date("20230530")
        self.assertEqual(result, datetime.date(2023, 5, 30))

    def test_should_accept_date_not_zero_padded(self):
        result = parse_date("2023-5-3")
        self.assertEqual(result, datetime.date(2023, 5, 3))
        result = parse_date("2023/5/3")
        self.assertEqual(result, datetime.date(2023, 5, 3))

    def test_should_accept_date_without_year(self):
        this_year = datetime.date.today().year
        result = parse_date("05-30")
        self.assertEqual(result, datetime.date(this_year, 5, 30))
        result = parse_date("05/30")
        self.assertEqual(result, datetime.date(this_year, 5, 30))
        result = parse_date("0530")
        self.assertEqual(result, datetime.date(this_year, 5, 30))

    def test_should_accept_date_without_year_and_not_zero_padded(self):
        this_year = datetime.date.today().year
        result = parse_date("5-3")
        self.assertEqual(result, datetime.date(this_year, 5, 3))
        result = parse_date("5/3")
        self.assertEqual(result, datetime.date(this_year, 5, 3))
        result = parse_date("503")
        self.assertEqual(result, datetime.date(this_year, 5, 3))

    def test_should_accept_relative_date(self):
        today = datetime.date.today()

        two_days_after = today + datetime.timedelta(days=2)
        result = parse_date("2 day")
        self.assertEqual(result, two_days_after)
        result = parse_date("2 days")
        self.assertEqual(result, two_days_after)
        result = parse_date("2d")
        self.assertEqual(result, two_days_after)

        four_weeks_after = today + datetime.timedelta(days=4 * 7)
        result = parse_date("4 week")
        self.assertEqual(result, four_weeks_after)
        result = parse_date("4 weeks")
        self.assertEqual(result, four_weeks_after)
        result = parse_date("4w")
        self.assertEqual(result, four_weeks_after)

        if today.month + 3 <= 12:
            three_months_after = datetime.date(today.year, today.month + 3, today.day)
        else:
            three_months_after = datetime.date(
                today.year + 1, today.month + 3 - 12, today.day
            )
        result = parse_date("3 month")
        self.assertEqual(result, three_months_after)
        result = parse_date("3 months")
        self.assertEqual(result, three_months_after)
        result = parse_date("3m")
        self.assertEqual(result, three_months_after)

    def test_should_accept_relative_date_keyword(self):
        today = datetime.date.today()

        tomorrow = today + datetime.timedelta(days=1)
        result = parse_date("tomorrow")
        self.assertEqual(result, tomorrow)

        yesterday = today - datetime.timedelta(days=1)
        result = parse_date("yesterday")
        self.assertEqual(result, yesterday)

    def test_should_accept_week_day(self):
        today = datetime.date.today()
        weekdays = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        for i, d in enumerate(weekdays):
            # Next monday/tuesday/... is expected
            result = parse_date(d)
            self.assertEqual(result.weekday(), i)
            self.assertTrue(0 <= (result - today).days < 7)

    def test_should_not_case_sensitive(self):
        today = datetime.date.today()

        result = parse_date("4D")
        self.assertEqual(result, today + datetime.timedelta(days=4))

        if today.month + 6 <= 12:
            expected = today.replace(month=today.month + 6)
        else:
            expected = today.replace(year=today.year + 1, month=today.month - 6)
        result = parse_date("6 Months")
        self.assertEqual(result, expected)

        result = parse_date("tOMOrrow")
        self.assertEqual(result, today + datetime.timedelta(days=1))

        result = parse_date("MoNDAy")
        self.assertEqual(result.weekday(), 0)
        self.assertTrue(0 <= (result - today).days < 7)

    def test_should_raise_value_error_for_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_date("unknown date")


class TestEditorParser(unittest.TestCase):
    def test_should_pick_up_all_four_fields(self):
        text = """
        Sample ToDo
        # sample/group
        ? 3 days

        This is the comment.
        """

        title, group, due_date, comment = parse_editor(text)
        self.assertEqual(title, "Sample ToDo")
        self.assertEqual(group, "sample/group")
        self.assertEqual(due_date, "3 days")
        self.assertEqual(comment, "This is the comment.")

    def test_text_may_lack_comment(self):
        text = """
        Sample ToDo
        # sample/group
        ? 3 days
        """

        title, group, due_date, comment = parse_editor(text)
        self.assertEqual(title, "Sample ToDo")
        self.assertEqual(group, "sample/group")
        self.assertEqual(due_date, "3 days")
        self.assertEqual(comment, "")

    def test_text_may_lack_group(self):
        text = """
        Sample ToDo
        ? 3 days

        This is the comment.
        """

        title, group, due_date, comment = parse_editor(text)
        self.assertEqual(title, "Sample ToDo")
        self.assertEqual(group, "")
        self.assertEqual(due_date, "3 days")
        self.assertEqual(comment, "This is the comment.")

    def test_text_may_lack_due_date(self):
        text = """
        Sample ToDo
        # sample/group

        This is the comment.
        """

        title, group, due_date, comment = parse_editor(text)
        self.assertEqual(title, "Sample ToDo")
        self.assertEqual(group, "sample/group")
        self.assertEqual(due_date, "")
        self.assertEqual(comment, "This is the comment.")

    def test_comment_may_be_very_long(self):
        text = """
        Sample ToDo

        This is a very very very very long comment
        that takes 2 lines.
        """

        _, _, _, comment = parse_editor(text)
        self.assertEqual(
            comment,
            "This is a very very very very long comment\nthat takes 2 lines.",
        )

    def test_should_ignore_after_double_slash(self):
        text = """
        Sample ToDo

        Before // after
        """

        title, group, due_date, comment = parse_editor(text)
        self.assertEqual(title, "Sample ToDo")
        self.assertEqual(group, "")
        self.assertEqual(due_date, "")
        self.assertEqual(comment, "Before")

    def test_should_raise_syntax_error(self):
        with self.assertRaises(SyntaxError):
            parse_editor("")
        with self.assertRaises(SyntaxError):
            parse_editor("""
            Sample ToDo
            Comment without inserting a new line.
            """)
