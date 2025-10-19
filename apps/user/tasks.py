


from celery import shared_task
from django.core.mail import send_mail, mail_admins
from django.contrib.auth.models import User
from django.conf import settings
from django.db import connection
from django.utils import timezone


@shared_task
def send_notify_have_new_user(username, email):
    subject = f"cảm ơn {username} đã đăng kí"
    message = f"email của bạn đăng kí là {email}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject = subject, message=message, from_email=from_email, recipient_list=recipient_list)



@shared_task
def check_db_health():
    """
    Tác vụ kiểm tra sức khỏe của database.
    Nếu kết nối thất bại, gửi email cảnh báo cho ADMINS.
    """
    try:
        # Thực hiện một query đơn giản để kiểm tra kết nối
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("Database connection thì khỏe.")
        return "Database is OK rồi đó"
    except Exception as e:
        # Nếu có lỗi, gửi email cảnh báo
        subject = 'CRITICAL: Database Health Check Failed!'
        message = (
            'The application failed to connect to the database.\n'
            'Please investigate immediately.\n\n'
            f'Error details: {e}'
        )
        # Hàm mail_admins sẽ tự động gửi email tới danh sách ADMINS trong settings.py
        mail_admins(subject, message)
        print(f"Sent critical alert: DB health check failed! Error: {e}")
        return f"Database check failed: {e}"

@shared_task
def send_daily_signup_report():
    """
    Tác vụ gửi báo cáo hàng ngày về những người dùng mới đã đăng ký.
    """
    # Lấy thời điểm bắt đầu của ngày hôm nay (00:00:00)
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Lấy những user được tạo từ đầu ngày hôm nay đến bây giờ
    new_users = User.objects.filter(date_joined__gte=today_start)

    subject = f'Daily User Signup Report - {today_start.strftime("%Y-%m-%d")}'

    if not new_users.exists():
        message = "No new users signed up today."
    else:
        user_list_str = "\n".join(
            [f"- Username: {user.username}, Email: {user.email}, Joined: {user.date_joined.strftime('%H:%M:%S')}" for user in new_users]
        )
        message = (
            f'Hello Admin,\n\n'
            f'Here is the list of users who signed up today ({today_start.strftime("%Y-%m-%d")}):\n\n'
            f'{user_list_str}\n\n'
            f'Total new users: {new_users.count()}'
        )

    mail_admins(subject, message)
    print(f"Daily signup report sent. New users: {new_users.count()}.")
    return f"Report sent for {new_users.count()} new users."