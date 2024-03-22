from django.shortcuts import render,get_object_or_404
from .models import FileScan, URLScan
from .scanners import VirusTotalAPI
from SecureZen.settings import VIRUSTOTAL_API_KEY
from django.contrib.auth.decorators import login_required
from secure.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

def upload_file(request):
    print("Entering upload_file function")
    context = {'scan_result': None, 'button_in_use': False, 'report_ready': False, 'total_vendors': 0, 'breaches_found': 0, 'error': None}
    
    if request.method == 'POST' and request.FILES.get('document'):
        context['button_in_use'] = True
        uploaded_file = request.FILES['document']
        vt_api = VirusTotalAPI(VIRUSTOTAL_API_KEY)
        try:
            file_content = uploaded_file.read()
            upload_response = vt_api.upload_file(file_content, uploaded_file.name)
                
            if upload_response.get('response_code') == 1:
                scan_id = upload_response.get('scan_id')
                scan_result = vt_api.get_automatic_report(scan_id)
                context['scan_result'] = scan_result
                total_vendors, breaches_found = process_scan_result(scan_result)
                context['report_ready'] = True
                context['total_vendors'] = total_vendors
                context['breaches_found'] = breaches_found
                
                # Save in database only if the user is authenticated
                if request.user.is_authenticated:
                    file_scan = FileScan(user=request.user, file_name=uploaded_file.name, scan_id=scan_id, scan_result=scan_result)
                    file_scan.save()
            else:
                context['error'] = "File upload to VirusTotal failed."
        except Exception as e:
            context['error'] = str(e)

    return render(request, 'scanner/upload_and_report.html', context)

# URL scanner

def scan_url(request):
    print("scan_url view was called")
    # Initialize additional context for total vendors and breaches found
    context = {'scan_result': None, 'button_in_use': False, 'report_ready': False,'total_vendors': 0, 'breaches_found': 0, 'error': None}
    print(context)
    
    if request.method == 'POST' and request.POST.get('url'):
        context['button_in_use'] = True
        submitted_url = request.POST['url']
        vt_api = VirusTotalAPI(VIRUSTOTAL_API_KEY)
        try:
            scan_response = vt_api.scan_url(submitted_url)
               
                # Save the URL scan result to the database
            if scan_response.get('response_code') == 1:
                scan_id = scan_response.get('scan_id')
                scan_result = vt_api.get_automatic_url_report(scan_id, interval=10, timeout=60)
                context['scan_result'] = scan_result
                total_vendors, breaches_found = process_scan_result(scan_result)
                context['report_ready'] = True
                context['total_vendors'] = total_vendors
                context['breaches_found'] = breaches_found
                
                # Save in database only if the user is authenticated
                if request.user.is_authenticated:
                    url_scan = URLScan(user=request.user, url=submitted_url, scan_id=scan_id, scan_result=scan_result)
                    url_scan.save()
            else:
                #context['scan_result'] = {}
                context['error'] = "URL scan submission failed."
        except Exception as e:
            #context['scan_result'] = {}
            context['error'] = str(e)
    print(context)        

    return render(request, 'scanner/scan_url.html', context)

def process_scan_result(scan_result):
    scans = scan_result.get('scans', {})
    total_vendors = len(scans)
    breaches_found = sum(1 for vendor, result in scans.items() if result.get('detected', False))
    return total_vendors, breaches_found

@login_required
def user_urls(request,username):
    user = get_object_or_404(User,username=username)
    urls = URLScan.objects.filter(user=user).all()
    return render(request, 'scanner/user_urls.html', {'user': user, 'urls': urls})

@login_required
def user_files(request,username):
    user = get_object_or_404(User, username=username)
    files = FileScan.objects.filter(user=user).all()
    return render(request, 'scanner/user_files.html', {'user': user, 'files': files})