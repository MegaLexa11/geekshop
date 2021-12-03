import requests

from datetime import datetime
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from django.conf import settings

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    url_method = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about', 'photo_200_orig'])

    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'

    responce = requests.get(api_url)

    if responce.status_code != 200:
        return

    data = responce.json()['response'][0]

    print('http' in data['photo_200_orig'])

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        else:
            user.age = age

    if data['photo_200_orig']:
        photo_data = requests.get(data['photo_200_orig'])
        photo_path = f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpeg'
        with open(photo_path, 'wb') as photo_file:
            photo_file.write(photo_data.content)
        user.avatar = photo_path

    user.save()
