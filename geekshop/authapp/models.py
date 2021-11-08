from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(verbose_name='аватар', upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')
    is_active = models.BooleanField(default=True)



