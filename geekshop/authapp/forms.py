from datetime import datetime
import hashlib

import pytz
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from authapp.models import ShopUser, ShopUserProfile
from django import forms
from django.conf import settings


class ShopUserLoginForm(AuthenticationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'password')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        elif data > 100:
            raise forms.ValidationError('Слишком большой возраст!')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        for user in ShopUser.objects.all():
            if user.email == data:
                raise forms.ValidationError('Такой Email уже занят!')
        return data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activation_key = hashlib.sha1(user.email.encode('utf-8')).hexdigest()
        user.activation_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))

        user.save()
        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        elif data > 100:
            raise forms.ValidationError('Слишком большой возраст!')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        is_exists = ShopUser.objects.exclude(pk=self.instance.pk).filter(email=data).exists()
        if is_exists:
            raise forms.ValidationError('Такой Email уже занят!')
        return data


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        exclude = 'user',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
