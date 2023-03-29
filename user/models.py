from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='image_users',null=True,blank=True)

