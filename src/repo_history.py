from github import Github
from dotenv import load_dotenv
import os
import json
from datetime import date, datetime

""" get histor from prs and transform """


class RepoHistory:
    results = []

    def __init__(self):
        load_dotenv()
        self.token = os.environ.get("GITHUB_ACCESS_TOKEN")
        self.client = Github(self.token)

    def handle(self, repo_name):
        """ scan repo and get history """
        """ list repos in account """
        """ iterate on repos """
        """ interate on history """
        repo = self.get_client().get_repo(repo_name)
        for pr in repo.get_pulls(state="closed, open",
                                 sort="created", direction="desc").get_page(0):
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
        data['created_at'] = pr.created_at
        data['closed_at'] = pr.closed_at
        data['merged_at'] = pr.merged_at
        data['merge_commit_sha'] = pr.merge_commit_sha
        data['seconds_old'] = self.seconds_old(data)
        return data

    def seconds_old(self, pr_tranformed):
        """ created_at compared to merged_at or closed_at or today """
        created_at = pr_tranformed['created_at']
        if pr_tranformed['merged_at'] is not None:
            delta = pr_tranformed['merged_at'] - created_at
            return delta.total_seconds()
        elif pr_tranformed['merged_at'] is None and pr_tranformed['closed_at'] is not None:
            delta = pr_tranformed['closed_at'] - created_at
            return delta.total_seconds()
        else:
            delta = datetime.now() - created_at
            return delta.total_seconds()
