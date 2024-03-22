python3 -m venv env
source env/bin/activate

pip install django
pip install djangorestframework
pip install requests

django-admin startproject SecureZen
cd SecureZen

python manage.py startapp scanner

python manage.py makemigrations 
python manage.py migrate 

python manage.py createsuperuser                janne123

python manage.py runserver

http://localhost:8000/scanner/upload/
http://localhost:8000/scanner/scan-url/

# URL scan
**HTTP 204 = request was successful but URL is already known and recently scanned, and hence no new scan is initiated or no new data is available to return.**
**Have to scan new urls, scanning same ones won't give report**

# File Scan
**Even on virustotal.com a 1mb PDF takes about a minute to scan**

**settings.py**

Make sure DEBUG is set to False in production environments. While it's True in your settings, which is fine for development, it should be turned off in production for security reasons.
Static and Media Files:

In a production environment, you'll need to properly configure the handling of static files and media files. Currently, only STATIC_URL is defined. Consider adding configurations for STATIC_ROOT, MEDIA_URL, and MEDIA_ROOT.

Database Configuration:
For development, SQLite is fine, but for production, especially for applications dealing with file scanning and potentially sensitive data, you might want to use a more robust database system like PostgreSQL.
Since you're studying PostgreSQL, it might be beneficial to use it for this project to gain practical experience.

Allowed Hosts:
When you move to production, make sure to update ALLOWED_HOSTS with the actual hostname of your site.

Additional Security Settings:
Consider adding additional security settings such as SECURE_BROWSER_XSS_FILTER, X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF, etc., to enhance the security of your Django application.

Logging:
Setting up logging can be useful, especially for tracking errors and issues in production.

Time Zone:
Since you're in Berlin, Germany, consider setting TIME_ZONE to your local time zone, e.g., 'Europe/Berlin'.


                                                