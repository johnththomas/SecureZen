"""
URL configuration for SecureZen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from secure.views import index  # Import the index view
from django.conf.urls import handler404
from secure.views import custom_404

handler404 = 'secure.views.custom_404'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),  # Directly route the root URL to the index view
    path("", include(('secure.urls', 'secure'), namespace='secure')),  # General site routes
    path("api/v1/scanner/", include(('scanner.urls', 'scanner_api'), namespace='scanner_api')),  # API access
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)