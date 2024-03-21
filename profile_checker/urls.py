# profile_checker/urls.py
from django.urls import path
from .views import check_url_platform

urlpatterns = [
    path('check-url-platform/', check_url_platform, name='check_url_platform'),
]
