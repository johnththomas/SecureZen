import requests  # Importing the requests library to make HTTP requests.
import time  # Importing the time library to use sleep for intervals and time tracking.
from django.conf import settings  # Importing Django's settings module to access project settings.

class VirusTotalAPI:
    def __init__(self, api_key):
        """
        Initializes the VirusTotalAPI class with a provided API key.
        
        :param api_key: Your VirusTotal API key as a string. This is required for authentication.
        """
        self.api_key = api_key  # Storing the API key for later use in API requests.
        self.base_url = "https://www.virustotal.com/vtapi/v2/"  # Base URL for the VirusTotal API.

    # File scanner section

    def upload_file(self, file_content, file_name):
        """
        Uploads a file to VirusTotal for scanning.
        
        :param file_content: The content of the file to be scanned.
        :param file_name: The name of the file to be scanned.
        :return: A JSON response containing the scan ID and other details.
        """
        upload_url = self.base_url + "file/scan"  # Constructing the URL for file scanning.
        files = {'file': (file_name, file_content)}  # Preparing the file payload for the request.
        params = {'apikey': self.api_key}  # Adding the API key to the request parameters.
        response = requests.post(upload_url, files=files, data=params)  # Making the POST request to upload the file.
        return response.json()  # Returning the JSON response from the API.

    def get_file_report(self, resource):
        """
        Retrieves a file scan report from VirusTotal.
        
        :param resource: The unique resource identifier for the file scan, typically the scan ID.
        :return: A JSON response containing the scan report.
        """
        report_url = self.base_url + "file/report"  # Constructing the URL to get the file report.
        params = {'apikey': self.api_key, 'resource': resource}  # Setting request parameters with API key and resource.
        response = requests.get(report_url, params=params)  # Making the GET request to retrieve the file report.
        return response.json()  # Returning the JSON response.

    def get_automatic_report(self, scan_id, interval=15, timeout=300):
        """
        Automatically retrieves the file scan report, polling the API until the report is available or timeout is reached.
        
        :param scan_id: The scan ID returned from the file upload.
        :param interval: The time in seconds to wait between each poll. Default is 15 seconds.
        :param timeout: The total time in seconds to keep trying before giving up. Default is 300 seconds.
        :return: A JSON response with the scan report or an error message.
        """
        start_time = time.time()  # Recording the start time to calculate elapsed time.
        while (time.time() - start_time) < timeout:  # Looping until the timeout is reached.
            report = self.get_file_report(scan_id)  # Attempting to retrieve the file report.
            response_code = report.get('response_code')  # Extracting the response code from the report.
            # The following prints are for debugging purposes, showing the progress and response codes.
            print(f"Checking report for scan_id {scan_id}: Response Code = {response_code}")
            if response_code is not None:
                print(f"Report details: {report}")
            if response_code == 1:  # A response code of 1 means the report is ready.
                return report
            elif response_code == 0:  # A response code of 0 means there's an error.
                error_message = report.get('verbose_msg', 'Error in report response')
                print(f"Error in report response: {error_message}")
                return {'error': error_message}
            else:
                # Handling unexpected response codes.
                print(f"Unexpected response code received: {response_code}")
            time.sleep(interval)  # Waiting for the specified interval before checking again.
        print(f"Timeout exceeded for scan_id {scan_id}. Report not available yet.")
        return {'error': 'Timeout exceeded. Report not available yet.'}

    # URL scanner section
    
    def scan_url(self, url):
        """
        Submits a URL to VirusTotal for scanning.
        
        :param url: The URL to be scanned.
        :return: A JSON response containing the scan ID and other details, or a message indicating no new content.
        """
        scan_url = self.base_url + "url/scan"  # Constructing the URL to submit a URL for scanning.
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }  # Setting the content type for the request.
        data = {'apikey': self.api_key, 'url': url}  # Preparing the data payload with the API key and URL.
        try:
            response = requests.post(scan_url, headers=headers, data=data)  # Making the POST request to scan the URL.
            if response.status_code == 204:
                # Handling the scenario where there is no new content to report.
                return {'message': 'No new content to report. URL might have been recently scanned.'}
            return response.json()  # Returning the JSON response.
        except Exception as e:
            # Logging the exception for debugging purposes.
            print(f"Exception occurred: {e}")
            if response:
                print(f"HTTP Response Status: {response.status_code}")
                print(f"HTTP Response Text: {response.text}")
            raise  # Re-raising the exception for further handling.

    def get_url_report(self, resource, interval=5, timeout=300):
        """
        Polls for a URL scan report until it's available or the timeout is reached.
        
        :param resource: The unique resource identifier for the URL scan, typically the scan ID.
        :param interval: The time in seconds to wait between each poll. Default is 5 seconds.
        :param timeout: The total time in seconds to keep trying before giving up. Default is 300 seconds.
        :return: A JSON response with the scan report or an error message.
        """
        report_url = self.base_url + "url/report"  # Constructing the URL to get the URL report.
        params = {'apikey': self.api_key, 'resource': resource}  # Setting request parameters with API key and resource.
        start_time = time.time()  # Recording the start time.
        while (time.time() - start_time) < timeout:  # Looping until the timeout is reached.
            response = requests.get(report_url, params=params)  # Making the GET request to retrieve the URL report.
            report = response.json()  # Parsing the JSON response.
            if report.get('response_code') == 1:
                # If the report is available, return it.
                return report
            elif report.get('response_code') == 0:
                # If the report is not ready yet, wait and then continue the loop.
                time.sleep(interval)
                continue
            else:
                # Handling other unexpected response codes.
                return {'error': 'Unexpected response code', 'details': report}
        return {'error': 'Timeout exceeded. Report not available yet.'}

    def get_automatic_url_report(self, scan_id, interval=15, timeout=300):
        """
        Automatically retrieves the URL scan report, polling the API until the report is available or timeout is reached.
        
        :param scan_id: The scan ID returned from the URL scan submission.
        :param interval: The time in seconds to wait between each poll. Default is 15 seconds.
        :param timeout: The total time in seconds to keep trying before giving up. Default is 300 seconds.
        :return: A JSON response with the scan report or an error message.
        """
        start_time = time.time()  # Recording the start time for timeout management.
        while (time.time() - start_time) < timeout:  # Looping until the timeout is reached.
            report = self.get_url_report(scan_id)  # Attempting to retrieve the URL report.
            if report.get('response_code') == 1:
                # If the report is ready, return it.
                return report
            elif report.get('response_code') == -2:
                # If the report is still queued, wait and then continue the loop.
                time.sleep(interval)
                continue
            else:
                # Handling errors or other unexpected response codes.
                return {'error': report.get('verbose_msg', 'Error in report response')}
        return {'error': 'Timeout exceeded. Report not available yet.'}
