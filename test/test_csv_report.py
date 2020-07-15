import inspect
from freezegun import freeze_time
import sys
import json
import unittest
from src.csv_report import CSVReport
from os import path, remove
from unittest.mock import MagicMock, patch
script_dir = path.dirname(__file__)


class TestCSVReport(unittest.TestCase):
    def test_repo_to_json(self):
        """ test creating csv out of it """
        if path.exists("report.csv"):
            remove("report.csv")

        with open("test/fixtures/results.json", 'r') as data:
            data = json.load(data)
        client = CSVReport()
        client.process(data)

        self.assertTrue(path.exists("report.csv"))


if __name__ == '__main__':
    unittest.main()
