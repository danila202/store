from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    image = models.ImageField(upload_to='image_users',null=True,blank=True)
    is_verified_email = models.BooleanField(default=False)



class EmailVerification(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    uniq_code = models.UUIDField(unique=True)
    data_created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_email_verification(self):
        send_mail(
            'Subject here',
            'My first email.',
            'from@example.com',
            [self.user.email],
            fail_silently=False,
        )



