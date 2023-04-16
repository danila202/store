import uuid

from celery import shared_task

from datetime import timedelta
from django.utils import timezone

from .models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = timezone.now() + timedelta(hours=24)
    record = EmailVerification.objects.create(user=user, uniq_code=uuid.uuid4(), expiration=expiration)
    record.send_email_verification()
