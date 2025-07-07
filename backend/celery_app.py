from celery import Celery
from celery.schedules import crontab
import csv,os
import time
from datetime import timedelta
from app import app


from models import User
from mail import send_mail

celery = Celery('tasks',broker='redis://localhost:6379/0')

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False)

@celery.task
def generate_csv_task(data, user_id):
    time.sleep(10)  # Simulate a delay for the task
    # Ensure the static/user_id directory exists
    folder_path = f'static/{user_id}'
    os.makedirs(folder_path, exist_ok=True)

    # File name with timestamp for uniqueness (optional)
    filename = f'{folder_path}/report.csv'

    if data:
        with open(filename, mode='w', newline='') as f:
            
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            
            '''user = User.query.get(user_id)
            if user:
                send_mail(
                    user.email,
                    "Reservation Report Ready",
                    f"Hi {user.username},\n\nYour parking report is ready!\nDownload it here:\nhttp://127.0.0.1:5000/static/{user_id}/report.csv\n\n- Vehicle Parking App")'''

    return filename



@celery.task
def daily_remainders():
    
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.id != 1:  # Skip the admin user
                send_mail(user.email, "Daily Reminder", "This is your daily reminder to check your parking reservations.") 
            

celery.conf.beat_schedule = {
    'daily_remainders_mails': {
        'task': 'celery_app.daily_remainders',
        #'schedule':timedelta(seconds=10),
        'schedule': crontab(day_of_month=1,hour=9, minute=0),  #monthly at 9:00 AM
        }
    }