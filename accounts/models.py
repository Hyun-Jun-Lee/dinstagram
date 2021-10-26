from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    website_url = models.URLField(blank=True) # 없어도 됨
    bio = models.TextField(blank=True)