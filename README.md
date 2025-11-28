# 쓰레기 배출 알림 시스템

서울특별시 관악구, 금천구, 동작구의 쓰레기 수거 일정을 관리하고 사용자에게 알림을 제공하는 Django 기반 웹 애플리케이션입니다.

## 주요 기능

- 📅 **캘린더 뷰**: 지역별 쓰레기 수거 일정을 캘린더 형식으로 확인
- 📋 **분리수거 가이드**: 지역별 배출 시간, 장소, 방법 안내
- 🔔 **알림 설정**: 수거 전날/당일 알림 설정 (쿠키 기반 사용자 식별)
- 🗺️ **다중 지역 지원**: 관악구, 금천구, 동작구 지원

## 기술 스택

- **Backend**: Django 5.2.3+
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript

## 프로젝트 구조

```
burim/
├── burim/              # Django 프로젝트 설정
│   ├── settings.py      # 프로젝트 설정
│   └── urls.py          # URL 라우팅
├── pages/               # 메인 앱
│   ├── models.py        # 데이터베이스 모델
│   ├── views.py         # 뷰 함수
│   ├── admin.py         # 관리자 페이지 설정
│   ├── templates/       # HTML 템플릿
│   └── static/          # 정적 파일
├── requirements.txt     # Python 패키지 목록
└── manage.py           # Django 관리 스크립트
```

## 설치 및 실행

### 1. 사전 요구사항

- Python 3.8 이상
- MySQL 8.0 이상
- pip

### 2. 저장소 클론

```bash
git clone https://github.com/rlagydlf/burim.git
cd burim/burim
```

### 3. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. 패키지 설치

```bash
pip install -r requirements.txt
```

### 5. MySQL 데이터베이스 설정

#### 5-1. MySQL 데이터베이스 생성

```sql
CREATE DATABASE burim_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 5-2. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
DB_NAME=burim_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

또는 `burim/burim/settings.py`에서 직접 수정할 수 있습니다:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'burim_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### 6. 마이그레이션 실행

```bash
python manage.py migrate
```

### 7. 관리자 계정 생성

```bash
python manage.py createsuperuser
```

### 8. 초기 데이터 입력

Django 관리자 페이지(`http://127.0.0.1:8000/admin`)에서 다음 데이터를 입력하세요:

1. **Region (지역)**: 
   - `seoul-guanak` - 서울특별시 관악구
   - `seoul-geumcheon` - 서울특별시 금천구
   - `seoul-dongjak` - 서울특별시 동작구

2. **RegionSchedule (지역별 수거 일정)**: 각 지역별 배출 시간, 장소, 방법 등

### 9. 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000` 접속

## 사용 방법

### 캘린더 보기
- 메인 페이지에서 지역을 선택하면 해당 지역의 수거 일정을 캘린더로 확인할 수 있습니다.

### 분리수거 가이드
- 각 지역별 배출 시간, 장소, 방법을 확인할 수 있습니다.

### 알림 설정
- 알림 설정 페이지에서 지역 선택 및 알림 시간을 설정할 수 있습니다.
- 수거 전날 또는 당일 알림을 받을 수 있습니다.

## 문제 해결

### MySQL 연결 오류

**문제**: `mysqlclient` 설치 오류 (Windows)
- **해결**: Visual C++ Build Tools 설치 또는 미리 컴파일된 wheel 파일 사용
  - https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

**문제**: 데이터베이스 연결 실패
- `settings.py`의 데이터베이스 비밀번호 확인
- MySQL 서비스가 실행 중인지 확인
- 데이터베이스 이름이 정확한지 확인

### 기타 문제

- MySQL 서비스가 실행되지 않는 경우: Windows 서비스 관리자에서 MySQL80 서비스 시작
- 마이그레이션 오류: `python manage.py makemigrations` 후 `python manage.py migrate` 재실행

## 기여하기

이슈나 풀 리퀘스트를 환영합니다! 프로젝트 개선을 위한 제안이 있으시면 이슈를 등록해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
