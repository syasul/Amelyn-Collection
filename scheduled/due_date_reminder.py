from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from User.models import CustomUser as User
from services import email_service

def fetchDueOrders():
    # TODO: fetch orders that are due for payment
    pass

# simulate the reminder
def fetchUser():
    user = User.objects.filter(email="mitifi2108@oprevolt.com").first()
    remind(user)
    print('Reminder sent to: ', user.email)

def remind(user):
    email_service.EmailService().sendReminder(user, 1, 3)

def start():
    print('Scheduler started at: ', datetime.now())
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchUser, 'interval', seconds=60, id='fetchUser')
    scheduler.start()