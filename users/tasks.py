from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
import uuid

from .models import User, EmailVerification

@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(minutes=30)
    print(f'{user} | {expiration}')
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()