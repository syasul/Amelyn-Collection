from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from User.models import CustomUser as User
from services import email_service
from datetime import timedelta
from Order.models import Order

def startReminder():
    # TODO: fetch orders that are due for payment
    fiveDaysLater = datetime.now() + timedelta(days=5)
    dueOrders = Order.objects.filter(status='Delivered', end_date__lte=fiveDaysLater)
    for order in dueOrders:
        user = order.id_user
        daysLeft = (order.end_date - datetime.now().date()).days
        remind(user, order.id, daysLeft)
        print('Reminder sent to: ', user.email)

# simulate the reminder
def fetchUser():
    user = User.objects.filter(email="mitifi2108@oprevolt.com").first()
    remind(user)
    print('Reminder sent to: ', user.email)

def remind(user, orderId, daysLeft):
    email_service.EmailService().sendReminder(user, orderId, daysLeft)

def start():
    print('Scheduler started at: ', datetime.now())
    scheduler = BackgroundScheduler()
    scheduler.add_job(startReminder, 'interval', seconds=60, id='startReminder')
    scheduler.start()