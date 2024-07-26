
from django.shortcuts import redirect
from django.conf import settings
import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login
from task.models import User
from rest_framework.authtoken.models import Token

def facebook_login(request):
    facebook_auth_url = (
        'https://www.facebook.com/v10.0/dialog/oauth?'
        'response_type=code&'
        f'client_id={settings.FACEBOOK_APP_KEY}&'
        f'redirect_uri={settings.FACEBOOK_REDIRECT_URI}&'
        'scope=email,public_profile'
    )
    return redirect(facebook_auth_url)



def facebook_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Missing authorization code'})

    token_url = 'https://graph.facebook.com/v10.0/oauth/access_token'
    token_data = {
        'code': code,
        'client_id': settings.FACEBOOK_APP_KEY,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
    }

    token_r = requests.post(token_url, data=token_data)
    token_json = token_r.json()

    if 'access_token' not in token_json:
        return JsonResponse(token_json)

    access_token = token_json['access_token']

    user_info_url = 'https://graph.facebook.com/me'
    user_info_params = {
        'fields': 'id,name,email',
        'access_token': access_token
    }
    user_info_r = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_r.json()

    if user_info_r.status_code != 200:
        return JsonResponse({'error': 'Failed to retrieve user info', 'details': user_info})

    email = user_info.get('email')
    username = user_info.get('name')
    facebook_id = user_info.get('id')

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            'registration_method': 'facebook',
        }
    )

    if created:
        token = Token.objects.create(user=user)
    else:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'registration_method': user.registration_method,
        'created': created,
        'token': token.key
    })
