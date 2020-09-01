from src.repo_history import RepoHistory
from src.csv_report import CSVReport
from src.json_report import JSONReport
import json
import sys

if __name__ == "__main__":
    client = RepoHistory()
    repo = sys.argv[1]
    state = sys.argv[2]
    filename = repo.replace("pfizer/", "")
    filename = filename + "-" + state
    print(f"Filename: {filename}")
    print(f"Getting data from Github for repo {repo}")
    results = client.handle(repo, state)
    print("Got data from Github creating report")
    client = CSVReport()
    client.process(results, filename)
    output = JSONReport()
    output.process(results, filename)
    print("See report.csv for the results")
