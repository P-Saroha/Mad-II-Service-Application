from celery.schedules import crontab
from flask import current_app as app
from Backend.celery.tasks import email_reminder

celery_app = app.extensions['celery']

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # every 10 seconds
    # sender.add_periodic_task(10.0, email_reminder.s('students@gmail', 'reminder to login', '<h1> hello everyone </h1>') )

    # daily message at 6:55 pm, everyday
    sender.add_periodic_task(crontab(hour=22, minute=10), email_reminder.s('students@gmail', 'reminder to login', '<h1> hello everyone </h1>'), name='daily reminder' )

    # weekly messages
    sender.add_periodic_task(crontab(hour=22, minute=10, day_of_week='sunday'), email_reminder.s('students@gmail', 'reminder to login', '<h1> hello everyone </h1>'), name = 'weekly reminder' )