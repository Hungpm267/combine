# myproject/celery.py
import os
from celery import Celery

# Đặt biến môi trường mặc định để Celery biết dùng settings của project nào.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTrainingProgram.settings')

# Tạo một instance của Celery và đặt tên cho nó là tên project
app = Celery('DjangoTrainingProgram')

# Celery sẽ load các cấu hình từ file settings.py của Django.
# namespace='CELERY' nghĩa là tất cả các cài đặt của Celery trong settings.py
# phải bắt đầu bằng tiền tố 'CELERY_', ví dụ: CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động tìm tất cả các file tasks.py trong các app của bạn.
app.autodiscover_tasks()



from celery.schedules import crontab # Để lập lịch nâng cao

# Đây là phần quan trọng của CELERY BEAT
app.conf.beat_schedule = {
    
    'check-db-health-every-minute': {
        'task': 'apps.user.tasks.check_db_health',
        'schedule': crontab(),  # crontab() rỗng tương đương với mỗi phút
    },
    'send-signup-report-every-minutes': {
        'task': 'apps.user.tasks.send_daily_signup_report',
        # Cấu hình crontab để chạy mỗi 2 phút
        'schedule': crontab(), 
    },
}
