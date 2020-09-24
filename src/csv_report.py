import csv


class CSVReport():

    def process(self, json_report, filename):
        """ take the data and process it """
        """ iterate over and convert """
        report_name = "report-" + filename + ".csv"
        with open(report_name, "w", newline='') as report:
            writer = csv.writer(report, delimiter=",")
            writer.writerow(json_report[0].keys())
            for items in json_report:
                writer.writerow(items.values())
