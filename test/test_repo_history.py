import inspect
from freezegun import freeze_time
import sys
import json
import unittest
from src.repo_history import RepoHistory
import os
from collections import namedtuple
from datetime import date, datetime
script_dir = os.path.dirname(__file__)


def convert_to_object(data):
    return namedtuple('X', data.keys())(*data.values())


class TestRepoHistory(unittest.TestCase):

    def test_loads_env(self):
        """ get based on repo name """
        client = RepoHistory()
        self.assertIsNotNone(client.token)

    def test_results_for_repo(self):
        client = RepoHistory()
        results = client.handle("alnutile/blog")
        self.assertIsNotNone(results)

    def test_transform_pr(self):
        client = RepoHistory()
        with open(os.path.join(script_dir,  "fixtures/pr.json"), 'r') as data:
            pr = json.load(data)
        pr['merged_at'] = datetime.fromisoformat("2011-01-27T19:01:12")
        pr['created_at'] = datetime.fromisoformat("2011-01-24T19:01:12")
        pr['closed_at'] = None
        results = client.transform_pr(convert_to_object(pr))
        self.assertIsNotNone(results)
        self.assertEqual(
            "e5bd3914e2e596debea16f433f57875b5b90bcd6", results['merge_commit_sha'])

    def test_seconds_old_has_created_and_merged(self):
        client = RepoHistory()
        with open(os.path.join(script_dir,  "fixtures/pr.json"), 'r') as data:
            pr = json.load(data)
        pr['merged_at'] = datetime.fromisoformat("2011-01-27T19:01:12")
        pr['created_at'] = datetime.fromisoformat("2011-01-24T19:01:12")
        pr['closed_at'] = None
        pr_tranformed = client.transform_pr(convert_to_object(pr))
        seconds = client.seconds_old(pr_tranformed)
        self.assertEqual(259200.0, seconds)

    def test_seconds_old_has_created_and_closed(self):
        client = RepoHistory()
        with open(os.path.join(script_dir,  "fixtures/pr.json"), 'r') as data:
            pr = json.load(data)
        pr['merged_at'] = None
        pr['created_at'] = datetime.fromisoformat("2011-01-27T19:01:12")
        pr['closed_at'] = datetime.fromisoformat("2011-01-29T19:01:12")
        pr_tranformed = client.transform_pr(convert_to_object(pr))
        seconds = client.seconds_old(pr_tranformed)
        self.assertEqual(172800.0, seconds)

    def test_not_closed_or_merged(self):
        client = RepoHistory()
        with open(os.path.join(script_dir,  "fixtures/pr.json"), 'r') as data:
            pr = json.load(data)
        pr['merged_at'] = None
        pr['created_at'] = datetime.fromisoformat("2011-01-27T19:01:12")
        pr['closed_at'] = None
        with freeze_time("2011-01-29T19:01:12"):
            pr_tranformed = client.transform_pr(convert_to_object(pr))
            seconds = client.seconds_old(pr_tranformed)
            self.assertEqual(172800.0, seconds)


if __name__ == '__main__':
    unittest.main()
