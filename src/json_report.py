import json

class JSONReport():

    def process(self, data, filename):
        report_name = "report_json-" + filename + ".json"
        with open(report_name, "w", newline='') as report:
            json.dump(data, report, indent=4, default=str)
        