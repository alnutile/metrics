from github import Github
from dotenv import load_dotenv
import os
import json
from datetime import date, datetime, timedelta
from src.seconds_diff import SecondsDiff
import csv
from csv import DictReader
""" get history from prs and transform """


class RepoHistory:
    results = []

    def __init__(self):
        load_dotenv()
        self.seconds_diff = SecondsDiff()
        self.token = os.environ.get("GITHUB_ACCESS_TOKEN")
        self.client = Github(self.token)

    def handle(self, repo_name, state):
        """ scan repo and get history """
        """ list repos in account """
        """ iterate on repos """
        """ interate on history """
        report_name = repo_name.replace("pfizer/", "")
        report_name = "report-" + report_name + "-" + state + ".csv"
        repo = self.get_client().get_repo(repo_name)
        for pr in repo.get_pulls(state=state,
                                 sort="created", direction="desc"):
            self.results.append(self.transform_pr(pr))
        # return the updated list to overwrite the previous one
        return self.update_lists(self.create_old_csv_dict(report_name), self.results)

    def get_client(self):
        return self.client

    def transform_pr(self, pr):
        if pr.title.startswith("["):
            jira_ticket = pr.title.split("]")[0][1:]
        else:
            jira_ticket = "-"

        data = {}
        data['id'] = pr.id
        data['jira_ticket'] = jira_ticket
        data['title'] = pr.title.rpartition(']')[2]
        data['state'] = pr.state
        data['number'] = pr.number
        data['labels'] = pr.labels
        data['created_at'] = pr.created_at
        data['closed_at'] = pr.closed_at
        data['merged_at'] = pr.merged_at
        data['merge_commit_sha'] = pr.merge_commit_sha
        data['duration'] = self.seconds_old(data)
        data["seconds"] = data["duration"].total_seconds()
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
            """ self.seconds_diff.office_time_between(created_at, pr_tranformed['merged_at']) """
            return self.seconds_diff.total_time_between(created_at, pr_tranformed['merged_at'])
        elif pr_tranformed['merged_at'] is None and pr_tranformed['closed_at'] is not None:
            """ //self.seconds_diff.office_time_between(created_at, pr_tranformed['closed_at']) """
            return self.seconds_diff.total_time_between(created_at, pr_tranformed['closed_at'])
        else:
            return self.seconds_diff.total_time_between(created_at, datetime.utcnow())

    # read the previous csv in same format as github json

    def create_old_csv_dict(self, report_name):
        with open(report_name, 'r') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            dict_reader = DictReader(read_obj)
            # get a list of dictionaries from dct_reader
            old_csv_list = list(dict_reader)
            # print list of dict i.e. rows

        return old_csv_list

    # compare the id's of previous csv with github json, append if id does not exist, else update
    def update_lists(self, old_csv_list, results):
        for json_pr in results:
            # flag to check if value exists in github json
            exists = False
            for index, csv_pr in enumerate(old_csv_list):
                if str(json_pr["id"]) == csv_pr["id"]:
                    old_csv_list[index] = json_pr
                    exists = True
                    break
        if exists == False:
            old_csv_list.append(json_pr)
        # here should return the updated list
        return old_csv_list
