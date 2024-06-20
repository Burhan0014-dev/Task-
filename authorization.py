import requests

from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from task.models import Users
from task.models import Users  
from rest_framework.authtoken.models import Token


def google_login(request):
    google_auth_url = (
        'https://accounts.google.com/o/oauth2/auth?'
        'response_type=code&'
        f'client_id={settings.GOOGLE_CLIENT_ID}&'
        f'redirect_uri={settings.GOOGLE_REDIRECT_URI}&'
        'scope=email%20profile'
    )
    return redirect(google_auth_url)


def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Missing authorization code'})

    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_r = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_r.json()

    if 'access_token' not in token_json:
        return JsonResponse(token_json) 

    access_token = token_json['access_token']


    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    user_info_params = {'access_token': access_token}
    user_info_r = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_r.json()

    if user_info_r.status_code != 200:
        return JsonResponse({'error': 'Failed to retrieve user info', 'details': user_info})

    email = user_info.get('email')
    username = user_info.get('name')  
    google_id = user_info.get('id')

    try:
        user = Users.objects.get(email=email)
        created = False
    except Users.DoesNotExist:
        user = Users.objects.create(
            email=email,
            username=username,
            registration_method='google',
        )
        token = Token.objects.create(user=user)
        created = True

    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'registration_method': user.registration_method,
        'created': created,
        'token': token.key if created else None
    })





