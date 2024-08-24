# profile_checker/urls.py
from django.urls import path
from .views import check_url_platform

urlpatterns = [
    path('check-url-platform/<str:platform>/<str:username>/', check_url_platform, name='check_url_platform'),
]
