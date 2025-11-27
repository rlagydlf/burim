from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import NotificationSetting, Region, RegionSchedule
from datetime import datetime, timedelta

def index(request):
    """홈페이지 - 지역 목록 표시"""
    regions = Region.objects.filter(is_active=True).order_by('name')
    context = {
        'regions': regions,
    }
    return render(request, 'pages/index.html', context)

def calendar(request):
    """캘린더 페이지 - 지역별 수거 일정을 캘린더로 표시"""
    regions = Region.objects.filter(is_active=True).order_by('name')
    region_schedules = {}
    waste_schedule_json = {}
    
    # 지역별 수거 일정 데이터 준비
    for region in regions:
        schedule = RegionSchedule.objects.filter(region=region).first()
        if schedule:
            # 템플릿에 전달할 지역별 정보
            region_schedules[region.code] = {
                'name': region.name,
                'discharge_time': schedule.discharge_time,
                'residential_area_time': schedule.residential_area_time,
                'commercial_area_time': schedule.commercial_area_time,
                'discharge_location': schedule.discharge_location,
                'discharge_method': schedule.discharge_method,
                'special_note': schedule.special_note,
                'contact': schedule.contact,
            }
            # JavaScript에서 사용할 수거 일정 (요일별)
            recyclable_days = []
            if region.code == 'seoul-guanak':
                recyclable_days = [4]  # 관악구: 목요일만
            elif region.code == 'seoul-geumcheon':
                recyclable_days = [0, 1, 2, 3, 4, 5]  # 금천구: 일~금
            elif region.code == 'seoul-dongjak':
                recyclable_days = [0, 4]  # 동작구: 일요일, 목요일
            
            # 일반쓰레기는 모든 지역 토요일 제외 고정
            waste_schedule_json[region.code] = {
                'days': [0, 1, 2, 3, 4, 5],  # 일~금
                'pattern': ['general', 'recyclable'],
                'recyclable_days': recyclable_days
            }
        else:
            # DB에 없으면 기본값 사용
            default_schedules = {
                'seoul-guanak': {'days': [0, 1, 2, 3, 4, 5], 'pattern': ['general', 'recyclable'], 'recyclable_days': [4]},
                'seoul-geumcheon': {'days': [0, 1, 2, 3, 4, 5], 'pattern': ['general', 'recyclable'], 'recyclable_days': [0, 1, 2, 3, 4, 5]},
                'seoul-dongjak': {'days': [0, 1, 2, 3, 4, 5], 'pattern': ['general', 'recyclable'], 'recyclable_days': [0, 4]},
            }
            if region.code in default_schedules:
                waste_schedule_json[region.code] = default_schedules[region.code]
    
    context = {
        'regions': regions,
        'region_schedules': region_schedules,
        'waste_schedule_json': json.dumps(waste_schedule_json),
    }
    return render(request, 'pages/calendar.html', context)

def guide(request):
    """분리수거 가이드 페이지 - 지역별 배출 방법 안내"""
    regions = Region.objects.filter(is_active=True).order_by('name')
    region_schedules = {}
    for region in regions:
        schedule = RegionSchedule.objects.filter(region=region).first()
        if schedule:
            region_schedules[region.code] = {
                'name': region.name,
                'discharge_time': schedule.discharge_time,
                'residential_area_time': schedule.residential_area_time,
                'commercial_area_time': schedule.commercial_area_time,
                'discharge_location': schedule.discharge_location,
                'discharge_method': schedule.discharge_method,
                'special_note': schedule.special_note,
                'contact': schedule.contact,
            }
    context = {
        'regions': regions,
        'region_schedules': region_schedules,
    }
    return render(request, 'pages/guide.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def save_notification_setting(request):
    """알림 설정 저장 API"""
    try:
        data = json.loads(request.body)
        # 사용자 식별자 가져오기 (쿠키 또는 헤더)
        user_id = request.COOKIES.get('user_id') or request.META.get('HTTP_X_USER_ID')
        if not user_id:
            import uuid
            user_id = str(uuid.uuid4())
        
        # 알림 설정 저장 또는 업데이트
        setting, created = NotificationSetting.objects.get_or_create(
            session_key=user_id,
            defaults={
                'region': data.get('region', ''),
                'enabled': data.get('enabled', True),
                'notify_before': data.get('notify_before', True),
                'notify_day': data.get('notify_day', True),
                'notification_time': data.get('notification_time', '20:00'),
            }
        )
        
        if not created:
            # 기존 설정 업데이트
            setting.region = data.get('region', setting.region)
            setting.enabled = data.get('enabled', setting.enabled)
            setting.notify_before = data.get('notify_before', setting.notify_before)
            setting.notify_day = data.get('notify_day', setting.notify_day)
            setting.notification_time = data.get('notification_time', setting.notification_time)
            setting.save()
        
        response = JsonResponse({'success': True, 'message': '알림 설정이 저장되었습니다.', 'session_key': user_id})
        response.set_cookie('user_id', user_id, max_age=365*24*60*60)  # 1년
        return response
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@require_http_methods(["GET"])
def get_notification_setting(request):
    """알림 설정 조회 API"""
    try:
        # 사용자 식별자로 알림 설정 조회
        user_id = request.COOKIES.get('user_id') or request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return JsonResponse({'success': True, 'setting': None})
        
        setting = NotificationSetting.objects.filter(session_key=user_id).first()
        
        if setting:
            return JsonResponse({
                'success': True,
                'setting': {
                    'region': setting.region,
                    'enabled': setting.enabled,
                    'notify_before': setting.notify_before,
                    'notify_day': setting.notify_day,
                    'notification_time': str(setting.notification_time),
                }
            })
        else:
            return JsonResponse({'success': True, 'setting': None})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@require_http_methods(["GET"])
def get_upcoming_collections(request):
    """다가오는 수거일 조회 API - 알림용"""
    try:
        # 사용자 알림 설정 조회
        user_id = request.COOKIES.get('user_id') or request.META.get('HTTP_X_USER_ID')
        if not user_id:
            return JsonResponse({'success': True, 'collections': []})
        
        setting = NotificationSetting.objects.filter(session_key=user_id, enabled=True).first()
        if not setting or not setting.region:
            return JsonResponse({'success': True, 'collections': []})
        
        # 지역별 수거 일정 가져오기
        region = Region.objects.filter(code=setting.region, is_active=True).first()
        if not region:
            return JsonResponse({'success': True, 'collections': []})
        
        # 지역별 재활용품 배출 요일 설정
        recyclable_days = []
        if setting.region == 'seoul-guanak':
            recyclable_days = [4]  # 관악구: 목요일만
        elif setting.region == 'seoul-geumcheon':
            recyclable_days = [0, 1, 2, 3, 4, 5]  # 금천구: 일~금
        elif setting.region == 'seoul-dongjak':
            recyclable_days = [0, 4]  # 동작구: 일요일, 목요일
        
        schedule = {
            'days': [0, 1, 2, 3, 4, 5],  # 일반쓰레기: 일~금
            'pattern': ['general', 'recyclable'],
            'recyclable_days': recyclable_days
        }
        
        # 다음 7일 중 수거일 확인
        today = datetime.now().date()
        collections = []
        for i in range(7):
            check_date = today + timedelta(days=i)
            day_of_week = check_date.weekday()  # 0=월요일, 6=일요일
            js_day = (day_of_week + 1) % 7  # JavaScript 요일로 변환 (0=일요일)
            
            if js_day in schedule['days']:
                # 쓰레기 종류 판단
                if js_day in recyclable_days:
                    waste_type = '재활용품'
                else:
                    waste_type = '일반쓰레기'
                
                # 알림 조건 확인 (전날 또는 당일)
                days_until = i
                if (setting.notify_before and days_until == 1) or (setting.notify_day and days_until == 0):
                    collections.append({
                        'date': check_date.strftime('%Y-%m-%d'),
                        'waste_type': waste_type,
                        'days_until': days_until,
                    })
        
        return JsonResponse({'success': True, 'collections': collections})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
