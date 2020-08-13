import json

class JSONReport():

    def process(self, data):
        with open("report_json.json", "w", newline='') as report:
            json.dump(data, report, indent=4, default=str)
        