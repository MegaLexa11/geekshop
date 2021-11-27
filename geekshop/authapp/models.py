import pytz
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.conf import settings


class ShopUser(AbstractUser):
    avatar = models.ImageField(verbose_name='аватар', upload_to='users_avatars', blank=True)
    avatar_url = models.CharField(max_length=128, null=True, blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=21)
    is_active = models.BooleanField(default=True)

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) >= self.activation_key_expired + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        self.is_active = True
        self.activation_key = None
        self.activation_key_expired = None
        self.save()


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    OTHERS = 'O'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (OTHERS, 'Иные'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=128, verbose_name='теги')
    aboutMe = models.TextField(max_length=512, blank=True, verbose_name='о себе')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='пол')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def update_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
