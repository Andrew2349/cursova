from django.contrib.auth.models import User, AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=1000)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    username = None
    REQUIRED_FIELDS = []
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/user.png')



