import time
from collections import defaultdict
from datetime import datetime

import requests
import yaml


class Endpoint:
    def __init__(self, name, url, method="GET", headers=None, body=None):
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers if headers else {}
        self.body = body

    def check_health(self):
        try:
            start_time = datetime.now()
            response = requests.request(
                self.method, self.url, headers=self.headers, data=self.body
            )
            latency = (
                datetime.now() - start_time
            ).total_seconds() * 1000  # Convert to milliseconds
            return 200 <= response.status_code < 300 and latency < 500
        except Exception as e:
            print(f"Error checking endpoint {self.name}: {e}")
            return False


class HealthMonitor:
    def __init__(self, config_file):
        self.endpoints = self.load_config(config_file)
        self.availability = defaultdict(lambda: {"up": 0, "total": 0})

    def load_config(self, config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        endpoints = []
        for entry in config:
            # Default to 'GET' if the 'method' key is not present
            method = entry.get("method", "GET").upper()  # Ensure method is uppercase
            endpoints.append(
                Endpoint(
                    name=entry["name"],
                    url=entry["url"],
                    method=method,
                    headers=entry.get("headers"),
                    body=entry.get("body"),
                )
            )
        return endpoints

    def run_checks(self):
        while True:
            for endpoint in self.endpoints:
                domain = endpoint.url.split("/")[2]  # Extract domain from URL
                result = endpoint.check_health()
                self.availability[domain]["total"] += 1
                if result:
                    self.availability[domain]["up"] += 1

            self.log_results()
            time.sleep(15)  # Wait for 15 seconds before next check

    def log_results(self):
        for domain, stats in self.availability.items():
            availability_pct = round(100.0 * stats["up"] / stats["total"])
            print(f"{domain} has {availability_pct}% availability percentage")


def main(config_file_path):
    monitor = HealthMonitor(config_file_path)
    try:
        monitor.run_checks()
    except KeyboardInterrupt:
        print("Program terminated by user.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python health_monitor.py test.yaml")
    else:
        main(sys.argv[1])
