# secure/urls.py
from django.urls import path
from .views import CustomLoginView, index, about, contact, registration, login, profile, logout_view


app_name = 'secure'

urlpatterns = [
    path('', index, name='index'),  # Adjusted for the root URL
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),  # Keep this if it's a different view or remove if using CustomLoginView for the same purpose
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', CustomLoginView.as_view(), name='custom_login'),  # Ensure CustomLoginView is imported
    # Removed duplicate 'accounts/profile/' if it's not needed or adjust as necessary
]
