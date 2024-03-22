from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'scanner'

schema_view = get_schema_view(
    openapi.Info(
        title='Virustotal API',
        default_version='v2',
        description='API for security',
        terms_of_service="https://www.virustotal.com/vtapi/v2/file/report?apikey={apikey}&resource={resource}",
        # contact=openapi.Contact(email="contact@example.com"),  # Specify a contact email if available
        # license=openapi.License(name="BSD License"),  # Specify a license name if applicable
    ),
    public=True,
    permission_classes=()
)

urlpatterns = [
    path('openapi/', schema_view.without_ui(cache_timeout=0), name='schema-openapi'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    path('upload/', views.upload_file, name='upload'),
    path('scan-url/', views.scan_url, name='scan-url'),
    path('user_urls/<str:username>/', views.user_urls, name='user_urls'),
    path('user_files/<str:username>/', views.user_files, name='user_files'),
]

