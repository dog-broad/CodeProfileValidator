# CodeProfileValidator/rating_checker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:user_id>/', views.user_detail, name='user_detail'),
    path('update_scores/<str:user_id>/', views.update_scores, name='update_scores'),
    path('fetch_platform_score/<str:platform>/<str:user_id>/', views.fetch_platform_score, name='fetch_platform_score'),
]
