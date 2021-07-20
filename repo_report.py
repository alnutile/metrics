from src.repo_history import RepoHistory
from src.csv_report import CSVReport
from src.json_report import JSONReport
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('repo', help='Name of the repo you want to run the report on')
    parser.add_argument('--state', dest="state", default="all", help='State of the PR request to run')
    parser.add_argument('--start', dest="start", default="", help='Start date for PRs')
    parser.add_argument('--end', dest="end", default="", help='End date for PRs')
    parser.add_argument('--teams-file', dest="teams-file", default="", help='File for github id to team mapping')

    args = parser.parse_args()
    repo = args.repo
    state = args.state
    start = args.start
    end = args.end

    client = RepoHistory()
    filename = repo.replace("pfizer/", "")
    filename = filename + "-" + state
    print(f"Filename: {filename}")
    print(f"Getting data from Github for repo {repo}")
    print(f"Start date is {start}")
    results = client.handle(repo, state, start, end)
    print("Got data from Github creating report")
    client = CSVReport()
    client.process(results, filename)
    output = JSONReport()
    output.process(results, filename)
    print(f"See report-{filename}.csv for the results")
