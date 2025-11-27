from django.db import models

class Region(models.Model):
    """지역 모델 - 관악구, 금천구, 동작구"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "지역"
        verbose_name_plural = "지역"

    def __str__(self):
        return self.name


class RegionSchedule(models.Model):
    """지역별 수거 일정 모델 - 배출 시간, 장소, 방법 등"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='schedules')
    
    # 배출 시간 정보
    discharge_time = models.CharField(max_length=200)
    residential_area_time = models.CharField(max_length=200, blank=True, null=True)
    commercial_area_time = models.CharField(max_length=200, blank=True, null=True)
    
    # 배출 장소 및 방법
    discharge_location = models.CharField(max_length=200)
    discharge_method = models.CharField(max_length=200)
    special_note = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=100)
    
    # 수거 일정 (JSON 형식)
    collection_days = models.JSONField(default=list)
    waste_pattern = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "지역별 수거 일정"
        verbose_name_plural = "지역별 수거 일정"
        unique_together = ['region']

    def __str__(self):
        return f"{self.region.name} 수거 일정"


class NotificationSetting(models.Model):
    """알림 설정 모델 - 사용자별 알림 옵션"""
    session_key = models.CharField(max_length=255, unique=True)
    region = models.CharField(max_length=50, choices=[
        ('seoul-guanak', '서울특별시 관악구'),
        ('seoul-geumcheon', '서울특별시 금천구'),
        ('seoul-dongjak', '서울특별시 동작구'),
    ], blank=True, null=True)
    enabled = models.BooleanField(default=True)
    notify_before = models.BooleanField(default=True)
    notify_day = models.BooleanField(default=True)
    notification_time = models.TimeField(default='20:00')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "알림 설정"
        verbose_name_plural = "알림 설정"

    def __str__(self):
        return f"{self.session_key} - {self.region}"
