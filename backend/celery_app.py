from celery import Celery
from celery.schedules import crontab
import csv,os
import time
from datetime import timedelta,datetime
from app import app
from models import User,Reservation
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
    filename = f'{folder_path}/reservations_report.csv'

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


@celery.task
def monthly_remainders():
    with app.app_context():
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            end_of_month = datetime(now.year + 1, 1, 1)
        else:
            end_of_month = datetime(now.year, now.month + 1, 1)

        users = User.query.all()

        for user in users:
            if user.id == 1:
                continue  # skip admin

            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parking_timestamp >= start_of_month,
                Reservation.parking_timestamp < end_of_month
            ).all()

            if not reservations:
                continue  # skip users with no reservations this month

            # Generate report data
            data = [{
                'username': r.user.username,
                'spot_number': r.spot.spot_number,
                'lot_location': r.spot.lot.location_name,
                'pincode': r.spot.lot.pin_code,
                'address': r.spot.lot.address,
                'parking_timestamp': r.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'leaving_timestamp': r.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.leaving_timestamp else '',
                'parking_cost': round(r.calculate_cost(), 2)
            } for r in reservations]

            # Trigger CSV generation asynchronously
            from celery_app import generate_csv_task
            filename = generate_csv_task.delay(data, user.id)

            # Send the email
            send_mail(
                    user.email,
                    "Your Monthly Parking Report",
                    f"Hi {user.username},\n\nYour parking report for {now.strftime('%B %Y')} is being prepared.\n"
                    f"It will be ready shortly at:\nhttp://127.0.0.1:5000/static/{user.id}/report.csv\n\n- Vehicle Parking App"
                    )


@celery.task
def generate_single_reservation_csv(reservation_id):
    from models import Reservation
    from app import app  # Needed for app context
    from flask import current_app

    with app.app_context():
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return None

        user_id = reservation.user_id
        folder_path = os.path.join('static', str(user_id))
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"reservation_{reservation_id}.csv")

        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Spot Number', 'Location', 'Parking Time', 'Leaving Time', 'Cost'])
            writer.writerow([
                reservation.user.username,
                reservation.spot.spot_number,
                reservation.spot.lot.location_name,
                reservation.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                reservation.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if reservation.leaving_timestamp else 'Still using',
                round(reservation.calculate_cost(), 2)
            ])

        return file_path



            

celery.conf.beat_schedule = {
    'daily_remainders_mails': {
        'task': 'celery_app.daily_remainders',
        #'schedule':timedelta(seconds=10),
        'schedule': crontab(hour=9, minute=0),  #daily at 9:00 AM
        },
    'monthly_report_mail': {
            'task': 'celery_app.monthly_remainders',
            'schedule': crontab(hour=10, minute=0, day_of_month='1'),  # 1st of every month at 10:00 AM
        }

    }