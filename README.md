# HTTP Endpoint Health Monitor
## Overview
This Python script continuously monitors the health of specified HTTP endpoints. It reads a list of endpoints from a YAML configuration file, periodically checks their availability based on response code and latency, and logs the cumulative availability percentage of each domain.
## Requirements
- Python 3.x 
- requests library 
- pyyaml library
## Configuration
Endpoints are defined in a YAML configuration file. Each entry in the file specifies the details of an HTTP endpoint:

name: A descriptive name for the endpoint.
url: The URL of the HTTP endpoint.
method: (Optional) The HTTP method (e.g., GET, POST). Defaults to GET if omitted.
headers: (Optional) A dictionary of HTTP headers to include in the request.
body: (Optional) The HTTP body for requests, primarily used with POST methods.



## Running the Script
- Ensure you have Python 3.x installed on your system. 
- Install the required libraries (requests and pyyaml). 
- Place your YAML configuration file in the same directory as the script or specify its path when running the script. 
- Run the script using the command:

`python health_monitor.py config.yaml`
- The script will start monitoring the endpoints and log the availability percentage every 15 seconds.

## Output
The script logs the availability percentage of each domain to the console after each 15-second monitoring cycle. The availability percentage is calculated based on the number of successful responses (HTTP 2xx status codes and response latency under 500 ms).

## Termination
To stop the script, use the keyboard interrupt (CTRL+C). The script will cease operations and exit.
