import requests
import time

class VirusTotalAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/vtapi/v2/"

    def upload_file(self, file_path):
        """
        Upload and scan a file.
        """
        upload_url = self.base_url + "file/scan"
        files = {'file': (file_path, open(file_path, 'rb'))}
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
            if report.get('response_code') == 1:
                return report
            time.sleep(interval)  

        return {'error': 'Timeout exceeded. Report not available yet.'}


if __name__ == "__main__":
    api_key = "YOUR_API_KEY"  
    vt_api = VirusTotalAPI(api_key)
    
    file_path = "/path/to/your/file"  
    
   
    upload_response = vt_api.upload_file(file_path)
    print("Upload Response:", upload_response)

    
    if upload_response.get('response_code') == 1:
        scan_id = upload_response.get('scan_id')
        report_response = vt_api.get_automatic_report(scan_id)
        print("Report Response:", report_response)
    else:
        print("Error in file upload.")
