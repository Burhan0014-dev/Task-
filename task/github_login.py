import requests
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import login
from task.models import Users  
from rest_framework.authtoken.models import Token

def github_login(request):
    github_auth_url = (
        'https://github.com/login/oauth/authorize?'
        f'client_id={settings.GITHUB_CLIENT_ID}&'
        f'redirect_uri={settings.GITHUB_REDIRECT_URI}&'
        'scope=user:email'
    )
    return redirect(github_auth_url)

def github_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'error': 'Missing authorization code'})

    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'code': code,
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'redirect_uri': settings.GITHUB_REDIRECT_URI,
    }
    token_headers = {'Accept': 'application/json'}

    token_r = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_r.json()

    if 'access_token' not in token_json:
        return JsonResponse(token_json)

    access_token = token_json['access_token']

    user_info_url = 'https://api.github.com/user'
    user_emails_url = 'https://api.github.com/user/emails'
    user_info_headers = {'Authorization': f'token {access_token}'}

    user_info_r = requests.get(user_info_url, headers=user_info_headers)
    user_info = user_info_r.json()

    user_emails_r = requests.get(user_emails_url, headers=user_info_headers)
    user_emails = user_emails_r.json()

    if user_info_r.status_code != 200 or user_emails_r.status_code != 200:
        return JsonResponse({'error': 'Failed to retrieve user info', 'details': user_info})

    email = next(email for email in user_emails if email['primary'])['email']
    username = user_info.get('login')
    github_id = user_info.get('id')

    user, created = Users.objects.get_or_create(
        email=email,
        defaults={
            'username': username,
            'registration_method': 'github',
        }
    )

    if created:
        token = Token.objects.create(user=user)
    else:
        token, _ = Token.objects.get_or_create(user=user)

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
