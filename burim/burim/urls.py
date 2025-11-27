"""URL configuration for burim project."""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from pages import views

def favicon_view(request):
    """favicon 요청 처리 (404 방지)"""
    return HttpResponse('', content_type='image/x-icon')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon_view),
    # 페이지
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('guide/', views.guide, name='guide'),
    # 알림 API
    path('api/notification/setting/', views.save_notification_setting, name='save_notification_setting'),
    path('api/notification/setting/get/', views.get_notification_setting, name='get_notification_setting'),
    path('api/notification/collections/', views.get_upcoming_collections, name='get_upcoming_collections'),
]
