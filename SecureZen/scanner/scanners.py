import requests
import time
from django.conf import settings

class VirusTotalAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/vtapi/v2/"

# File scanner

    def upload_file(self, file_content, file_name):
        """
        Upload and scan a file.
        """
        upload_url = self.base_url + "file/scan"
        files = {'file': (file_name, file_content)}
        params = {'apikey': self.api_key}
        response = requests.post(upload_url, files=files, data=params)
        return response.json()

    def get_file_report(self, resource):
        """
        Retrieve file scan report.
        """
        report_url = self.base_url + "file/report"
        params = {'apikey': self.api_key, 'resource': resource}
        response = requests.get(report_url, params=params)
        return response.json()

    def get_automatic_report(self, scan_id, interval=15, timeout=300):
        """
        Automatically retrieve the report after scanning.
        Interval: Time (in seconds) between each check.
        Timeout: Total time (in seconds) to keep checking before giving up.
        """
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            report = self.get_file_report(scan_id)
            response_code = report.get('response_code')
            # Print the response code and other relevant details
            print(f"Checking report for scan_id {scan_id}: Response Code = {response_code}")
            if response_code is not None:
                print(f"Report details: {report}")
            if response_code == 1:
                return report
            elif response_code == 0:
                # Handle error in report response
                error_message = report.get('verbose_msg', 'Error in report response')
                print(f"Error in report response: {error_message}")
                return {'error': error_message}
            else:
                # Print unexpected response code
                print(f"Unexpected response code received: {response_code}")
            time.sleep(interval)  # Wait for the specified interval before checking again
        # Print timeout
        print(f"Timeout exceeded for scan_id {scan_id}. Report not available yet.")
        return {'error': 'Timeout exceeded. Report not available yet.'}

# URL scanner
    
    def scan_url(self, url):
        """
        Submit a URL for scanning.
        """
        scan_url = self.base_url + "url/scan"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'apikey': self.api_key, 'url': url}
        try:
            response = requests.post(scan_url, headers=headers, data=data)
            if response.status_code == 204:
                # Handle no content scenario
                return {'message': 'No new content to report. URL might have been recently scanned.'}
            return response.json()
        except Exception as e:
            # Log the exception along with response status and text for debugging
            print(f"Exception occurred: {e}")
            if response:
                print(f"HTTP Response Status: {response.status_code}")
                print(f"HTTP Response Text: {response.text}")
            raise  # Re-raise the exception to handle it further up the call stack

    def get_url_report(self, resource, interval=5, timeout=300):
        report_url = self.base_url + "url/report"
        params = {'apikey': self.api_key, 'resource': resource}
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            response = requests.get(report_url, params=params)
            report = response.json()
            if report.get('response_code') == 1:
                # Report is available
                return report
            elif report.get('response_code') == 0:
                # Report is not ready yet
                time.sleep(interval)
                continue
            else:
                # Handle other response codes
                return {'error': 'Unexpected response code', 'details': report}
        return {'error': 'Timeout exceeded. Report not available yet.'}
    
    def get_automatic_url_report(self, scan_id, interval=15, timeout=300):
        """
        Automatically retrieve the URL report after scanning.
        Interval: Time (in seconds) between each check.
        Timeout: Total time (in seconds) to keep checking before giving up.
        """
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            report = self.get_url_report(scan_id)
            if report.get('response_code') == 1:
                return report
            elif report.get('response_code') == -2:
                # Report is still queued
                time.sleep(interval)
                continue
            else:
                # Handle error or other response codes
                return {'error': report.get('verbose_msg', 'Error in report response')}
        return {'error': 'Timeout exceeded. Report not available yet.'}



