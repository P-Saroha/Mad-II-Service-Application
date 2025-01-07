from celery import shared_task 
import time
import flask_excel
from Backend.models import Customer, ServiceProfessional
from flask import current_app
import logging
import datetime
from Backend.celery.mail_service import send_email

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

@shared_task(ignore_result=False)
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task(bind=True, ignore_result=False)
def create_csv(self):
    try:
        # Fetch data from models
        professionals = ServiceProfessional.query.all()

        task_id = self.request.id

        professional_filename = f'ServiceProfessional_data_{task_id}.csv'

        # Define column names for model
        professional_columns = [column.name for column in ServiceProfessional.__table__.columns]


        # Generate CSV for ServiceProfessional model
        csv_out = flask_excel.make_response_from_query_sets(professionals, column_names=professional_columns, file_type='csv')
        with open(f'./Backend/celery/user-downloads/{professional_filename}', 'wb') as file:
            file.write(csv_out.data)

        # Log success
        logger.info(f"CSV files for all models (Customer, Service Professional, Service, Service Request) created successfully")

        # Return file paths
        return {
            "message": "CSV files for all models created successfully",
            "professional_file": professional_filename,
        }

    except Exception as e:
        logger.error(f"An error occurred while creating CSV files: {str(e)}")
        return {
            "message": "An error occurred while creating CSV files",
            "error": str(e)
        }

@shared_task(ignore_result=True)
def email_reminder(to, subject, content):
    send_email(to, subject, content)
