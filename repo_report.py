from src.repo_history import RepoHistory
from src.csv_report import CSVReport
import json
import sys

if __name__ == "__main__":
    client = RepoHistory()
    repo = sys.argv[1]
    print(f"Getting data from Github for repo {repo}")
    results = client.handle(repo)
    print("Got data from Github creating report")
    if isinstance(results, str):
        print(results) 
    else:
        client = CSVReport()
        client.process(results)
        print("See report.csv for the results")
