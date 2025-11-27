from django.contrib import admin
from .models import Region, RegionSchedule, NotificationSetting

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(RegionSchedule)
class RegionScheduleAdmin(admin.ModelAdmin):
    list_display = ['region', 'discharge_time', 'discharge_location', 'contact', 'updated_at']
    list_filter = ['region', 'updated_at']
    search_fields = ['region__name', 'discharge_location', 'contact']
    fieldsets = (
        ('기본 정보', {
            'fields': ('region',)
        }),
        ('배출 시간', {
            'fields': ('discharge_time', 'residential_area_time', 'commercial_area_time')
        }),
        ('배출 장소 및 방법', {
            'fields': ('discharge_location', 'discharge_method')
        }),
        ('특별 사항', {
            'fields': ('special_note',)
        }),
        ('연락처', {
            'fields': ('contact',)
        }),
        ('수거 일정 설정', {
            'fields': ('collection_days', 'waste_pattern'),
            'description': 'collection_days: [0,1,2,3,4] (0=일요일, 1=월요일, ...), waste_pattern: ["general", "recyclable", "food", ...]'
        }),
    )

@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'region', 'enabled', 'notify_before', 'notify_day', 'notification_time', 'created_at']
    list_filter = ['enabled', 'region', 'notify_before', 'notify_day']
    search_fields = ['session_key', 'region']
