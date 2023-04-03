from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from store.settings import DOMAIN_NAME, EMAIL_HOST_USER


class User(AbstractUser):
    image = models.ImageField(upload_to='image_users', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    uniq_code = models.UUIDField(unique=True)
    data_created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_email_verification(self):
        link = reverse('user:email_verify', kwargs={'email': self.user.email, 'uniq_code': self.uniq_code})
        verification_link = f'{DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для пользователя {self.user.username} '
        message = f'Для подтверждения учётной записи {self.user.email} перейдите по ссылке {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
