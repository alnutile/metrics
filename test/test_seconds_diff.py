import inspect
from freezegun import freeze_time
import sys
import json
import unittest
import os
from unittest.mock import MagicMock, patch
from collections import namedtuple
from datetime import date, datetime
from src.seconds_diff import SecondsDiff


class TestSecondsDiff(unittest.TestCase):
    def test_full_week(self):
        client = SecondsDiff()
        start = datetime.fromisoformat("2020-07-20:09:12")
        end = datetime.fromisoformat("2020-07-24:13:12")
        results = client.office_time_between(start, end)
        self.assertIsNotNone(results)
        self.assertEqual(results, 72000)

    def test_one_work_day(self):
        client = SecondsDiff()
        start = datetime.fromisoformat("2020-07-20:09:12")
        end = datetime.fromisoformat("2020-07-20:12:12")
        results = client.office_time_between(start, end)
        self.assertIsNotNone(results)
        # 3 hours
        # 180 mijutes
        # 180*60=10800
        # 1 8 hour work day is 28800 seconds
        self.assertEqual(results, 10800)

    def test_one_day_over_weekend(self):
        client = SecondsDiff()
        start = datetime.fromisoformat("2020-07-24:09:12")
        end = datetime.fromisoformat("2020-07-27:12:12")
        results = client.office_time_between(start, end)
        self.assertIsNotNone(results)
        self.assertEqual(results, 39600)
