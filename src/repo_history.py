from github import Github
from dotenv import load_dotenv
import os
import json
from datetime import date, datetime
from src.seconds_diff import SecondsDiff

""" get history from prs and transform """


class RepoHistory:
    results = []

    def __init__(self):
        load_dotenv()
        self.seconds_diff = SecondsDiff()
        self.token = os.environ.get("GITHUB_ACCESS_TOKEN")
        self.client = Github(self.token)

    def handle(self, repo_name):
        """ scan repo and get history """
        """ list repos in account """
        """ iterate on repos """
        """ interate on history """
        repo = self.get_client().get_repo(repo_name)
        for pr in repo.get_pulls(state="all",
                                 sort="created", direction="desc"):
            self.results.append(self.transform_pr(pr))
        return self.results

    def get_client(self):
        return self.client

    def transform_pr(self, pr):
        data = {}
        data['id'] = pr.id
        data['title'] = pr.title
        data['state'] = pr.state
        data['number'] = pr.number
        data['labels'] = pr.labels
        data['created_at'] = pr.created_at
        data['closed_at'] = pr.closed_at
        data['merged_at'] = pr.merged_at
        data['merge_commit_sha'] = pr.merge_commit_sha
        data['seconds_old'] = self.seconds_old(data)
        data['hours_old'] = (data['seconds_old'] / 3600)
        data['created_at'] = self.set_date_to_string(pr.created_at)
        data['closed_at'] = self.set_date_to_string(pr.closed_at)
        data['merged_at'] = self.set_date_to_string(pr.merged_at)
        return data

    def set_date_to_string(self, _date):
        if(_date is not None):
            return _date.strftime("%m/%d/%Y, %H:%M:%S")
        else:
            return None

    def seconds_old(self, pr_tranformed):
        """ created_at compared to merged_at or closed_at or today """
        created_at = pr_tranformed['created_at']
        if pr_tranformed['merged_at'] is not None:
            return self.seconds_diff.office_time_between(created_at, pr_tranformed['merged_at'])
        elif pr_tranformed['merged_at'] is None and pr_tranformed['closed_at'] is not None:
            return self.seconds_diff.office_time_between(created_at, pr_tranformed['closed_at'])
        else:
            return self.seconds_diff.office_time_between(created_at, datetime.now())
