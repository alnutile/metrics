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
        # 20 mon to 24 friday so not full work since 1pm to 1pm
        # more like 4 days and 4 hours
        # the work day is 8 hours
        # 4 * 8 = 32 hours
        # (32*60)*60 = 115200 seconds
        # 1 8 hour work day is 28800 seconds
        self.assertEqual(results.seconds, 57600)

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
        self.assertEqual(results.seconds, 10800)
