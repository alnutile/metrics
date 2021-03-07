from src.repo_history import RepoHistory
from src.csv_report import CSVReport
import json
import sys
import click


@click.command()
@click.option("--owner_repo", help="use foo/bar as the input make sure you have pull requests")
@click.option("--format", default="csv", help="Output as csv or json")
def run(owner_repo, format):
    client = RepoHistory()
    print(f"Getting data from Github for repo {owner_repo}")
    results = client.handle(owner_repo)
    print("Got data from Github creating report")
    if isinstance(results, str):
        print(results)
    elif format == "json":
        print("coming soon")
    else:
        client = CSVReport()
        client.process(results)
        print("See report.csv for the results")


if __name__ == "__main__":
    run()
