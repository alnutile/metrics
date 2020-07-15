import inspect
from freezegun import freeze_time
import sys
import json
import unittest
from src.repo_history import RepoHistory
import os
from github import Repository, Requester
from unittest.mock import MagicMock, patch
from collections import namedtuple
from datetime import date, datetime
script_dir = os.path.dirname(__file__)


def convert_to_object(data):
    return namedtuple('X', data.keys())(*data.values())


with open(os.path.join(script_dir,  "fixtures/prs.json"), 'r') as data:
    pr = json.load(data)


class TestRepoHistory(unittest.TestCase):

    def test_loads_env(self):
        """ get based on repo name """
        client = RepoHistory()
        self.assertIsNotNone(client.token)

    @unittest.skip("Just to help with understanding the api")
    def test_real_api(self):
        client = RepoHistory()
        results = client.handle("friendsofcat/laravel-feature-flag")
        """ get defaults """
        """ open and closed """
        """ get defaults by reverse """
        """ sort by created """
        """ get defaults but only one page reverse """
        self.assertIsNotNone(results)

    @patch("src.repo_history.Github")
    def test_results_for_repo(self, mock_github):
        client = RepoHistory()
        mock_github.get_pulls = MagicMock(return_value=Repository.Repository(
            Requester, [], pr, completed=True))
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
        self.assertEqual('01/24/2011, 19:01:12', results['created_at'])
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
        pr_tranformed['merged_at'] = datetime.fromisoformat(
            "2011-01-27T19:01:12")
        pr_tranformed['created_at'] = datetime.fromisoformat(
            "2011-01-24T19:01:12")
        pr_tranformed['closed_at'] = None
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
        pr_tranformed['merged_at'] = None
        pr_tranformed['created_at'] = datetime.fromisoformat(
            "2011-01-27T19:01:12")
        pr_tranformed['closed_at'] = datetime.fromisoformat(
            "2011-01-29T19:01:12")
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
            pr_tranformed['created_at'] = datetime.fromisoformat(
                "2011-01-27T19:01:12")
            seconds = client.seconds_old(pr_tranformed)
            self.assertEqual(172800.0, seconds)


if __name__ == '__main__':
    unittest.main()
