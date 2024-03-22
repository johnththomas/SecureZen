from django.shortcuts import render  # Importing Django's render function to render templates.
from .models import FileScan  # Importing the FileScan model to interact with the file scan database records.
from .scanners import VirusTotalAPI  # Importing the VirusTotalAPI class to use for scanning.
from django.conf import settings  # Importing Django's settings to access project configurations.
from django.http import HttpResponse  # Importing HttpResponse to return HTTP responses.

# File scanner

def upload_file(request):
    """
    View to handle the uploading and scanning of files.
    
    :param request: The HTTP request object.
    :return: Renders a template with the context containing scan results or an error message.
    """
    print("Entering upload_file function")  # Debug print statement.
    print(request.FILES)  # Debug print to show the files included in the request.
    context = {'scan_result': None, 'error': None}  # Initializing context dictionary with default values.
    if request.method == 'POST' and request.FILES.get('document'):
        # Checking if the request method is POST and if there's a document in FILES.
        uploaded_file = request.FILES['document']  # Accessing the uploaded file.
        file_scan = FileScan(file_name=uploaded_file.name)  # Creating a new FileScan instance with the uploaded file's name.
        file_scan.save()  # Saving the FileScan instance to the database.
        vt_api = VirusTotalAPI(settings.VIRUSTOTAL_API_KEY)  # Creating an instance of VirusTotalAPI with the API key from settings.
        try:
            file_content = uploaded_file.read()  # Reading the content of the uploaded file.
            upload_response = vt_api.upload_file(file_content, uploaded_file.name)  # Uploading the file to VirusTotal for scanning.
            if upload_response.get('response_code') == 1:
                # Checking if the upload was successful.
                file_scan.scan_id = upload_response.get('scan_id')  # Storing the scan ID in the FileScan instance.
                file_scan.scan_result = vt_api.get_automatic_report(file_scan.scan_id)  # Getting the scan result.
                file_scan.save()  # Saving the updated FileScan instance to the database.
                context['scan_result'] = file_scan.scan_result  # Adding the scan result to the context.
            else:
                context['error'] = "File upload to VirusTotal failed."  # Setting an error message if the upload failed.
        except Exception as e:
            context['error'] = str(e)  # Setting an error message in case of an exception.
    return render(request, 'scanner/upload_and_report.html', context)  # Rendering the template with the context.

# URL scanner

def scan_url(request):
    """
    View to handle the scanning of URLs.
    
    :param request: The HTTP request object.
    :return: Renders a template with the context containing URL scan results or an error message.
    """
    print("scan_url view was called")
    
    # Setting up a context dictionary to pass data to the template. Initially, it's empty for scan results and errors.
    context = {'scan_result': None, 'error': None}
    
    # Checking if the request method is POST and if there's a 'url' parameter in the POST data.
    if request.method == 'POST' and request.POST.get('url'):
        # Retrieving the submitted URL from the POST data.
        submitted_url = request.POST['url']
        # Logging the submitted URL for debugging purposes.
        print(f"Submitted URL: {submitted_url}")
        
        # Creating an instance of the VirusTotalAPI class, passing in the API key from settings.
        vt_api = VirusTotalAPI(settings.VIRUSTOTAL_API_KEY)
        try:
            # Using the scan_url method of the VirusTotalAPI instance to submit the URL for scanning.
            scan_response = vt_api.scan_url(submitted_url)
            # Logging the response from the scan_url method for debugging.
            print(f"Scan Response: {scan_response}")
            
            # Checking if the response code from the scan submission is 1 (which means submission was successful).
            if scan_response.get('response_code') == 1:
                # Retrieving the scan ID from the scan response.
                scan_id = scan_response.get('scan_id')
                # Fetching the scan result using the scan ID, with a specific interval and timeout.
                scan_result = vt_api.get_automatic_url_report(scan_id, interval=10, timeout=60)
                # Logging the scan result for debugging.
                print(f"Scan Result: {scan_result}")
                
                # Creating a new URLScan instance with the submitted URL, scan ID, and the scan result, then saving it to the database.
                url_scan = URLScan(url=submitted_url, scan_id=scan_id, scan_result=scan_result)
                url_scan.save()
                
                # Updating the context with the scan result to pass it to the template.
                context['scan_result'] = url_scan.scan_result
            else:
                # Setting an error message in the context if the URL scan submission failed.
                context['error'] = "URL scan submission failed."
                # Logging the error for debugging.
                print(f"Error in scan submission")
        except Exception as e:
            # Catching any exceptions that occur during the process, setting an error message in the context.
            context['error'] = str(e)
            # Logging the exception for debugging.
            print(f"Exception: {e}")
    
    # Rendering the 'scan_url.html' template, passing in the context dictionary with scan results or error message.
    return render(request, 'scanner/scan_url.html', context)
