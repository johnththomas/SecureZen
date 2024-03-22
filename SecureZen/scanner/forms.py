from django import forms
from .models import  FileScan, URLScan

class FileUploadForm(forms.ModelForm):
    document = forms.FileField()
    class Meta:
        model = FileScan
        fields = ['file_name','document']

class URLScanForm(forms.ModelForm):
    class Meta:
        model = URLScan
        fields = ['url',]
    