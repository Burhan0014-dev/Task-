import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from requests.models import Response
from rest_framework.authtoken.models import Token
from gcs.settings import GITHUB_CLIENT_ID, GITHUB_REDIRECT_URI
from task.models import User
from task.github_login import github_login, github_callback

User = get_user_model()

@pytest.mark.django_db
def test_github_login(mocker):
    """Tests redirect to Github login URL."""

    url = reverse('github_login')
    client = APIClient()

    mocked_response = Response()
    mocked_response.status_code = 200
    mocker.patch('requests.get', return_value=mocked_response)

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == f'https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=user:email'
             
@pytest.mark.django_db
def test_github_callback_missing_code(client):
    """Tests error response for missing authorization code."""

    url = reverse('github_callback')

    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {'error': 'Missing authorization code'}

@pytest.mark.django_db 
def test_github_callback_invalid_token_response(mocker, client):
    """Tests error handling for invalid token response."""

    url = reverse('github_callback')

    mocked_response = Response()
    mocker.patch.object(mocked_response, 'json', return_value={'error': 'invalid_request'})
    mocker.patch('requests.post', return_value=mocked_response)

    response = client.get(url, {'code': 'fake_code'})

    assert response.status_code == 200
    assert response.json().get('error') == 'invalid_request'

@pytest.mark.django_db
def test_github_callback_successful_login(mocker, client):
    """Tests successful login flow with mocked GitHub responses."""

    url = reverse('github_callback')

    access_token_response = Response()
    mocker.patch.object(access_token_response, 'json', return_value={'access_token': 'valid_access_token'})
    mocker.patch('requests.post', return_value=access_token_response)

    user_info_response = Response()
    mocker.patch.object(user_info_response, 'json', return_value={
        'id': '123456',
        'name': 'John Doe',
        'email': 'johndoe@example.com',
    })
    mocker.patch('requests.get', return_value=user_info_response)

    response = client.get(url, {'code': 'fake_code'})

    user, created = User.objects.get_or_create(
        email='johndoe@example.com',
        defaults={'username': 'John Doe'}
    )
    
    assert user.username == 'John Doe'
    assert user.email == 'johndoe@example.com'
    assert response.status_code == 200

User = get_user_model()

@pytest.mark.django_db
def test_github_callback_user_creation(mocker, client):
    """Test user creation during GitHub callback."""
    url = reverse('github_callback')
    code = 'fake_code'
    client.get(url, {'code': code})

    token_response = Response()
    token_response.status_code = 200
    token_response._content = b'{"access_token": "valid_access_token"}'
    mocker.patch('requests.post', return_value=token_response)

    user_info_response = Response()
    user_info_response.status_code = 200
    user_info_response._content = b'{"id": "123456", "login": "johndoe", "email": "johndoe@example.com"}'
    user_emails_response = Response()
    user_emails_response.status_code = 200
    user_emails_response._content = b'[{"email": "johndoe@example.com", "primary": true}]'

    mocker.patch('requests.get', side_effect=[user_info_response, user_emails_response])

    response = client.get(url, {'code': code})
    user = User.objects.get(email='johndoe@example.com')
    assert user.username == 'johndoe'
    assert user.registration_method == 'github'

    token = Token.objects.get(user=user)
    assert token.key is not None

    assert response.status_code == 200
    json_response = response.json()
    assert json_response['id'] == user.id
    assert json_response['username'] == user.username
    assert json_response['email'] == user.email
    assert json_response['registration_method'] == user.registration_method
    assert json_response['created'] is True
    assert json_response['token'] == token.key

@pytest.mark.django_db
def test_github_callback_existing_user(mocker, client):
    """Test existing user during GitHub callback."""

    user = User.objects.create_user(email='johndoe@example.com', username='johndoe', registration_method='github')
    token = Token.objects.create(user=user)

    url = reverse('github_callback')
    code = 'fake_code'
    client.get(url, {'code': code})

    token_response = Response()
    token_response.status_code = 200
    token_response._content = b'{"access_token": "valid_access_token"}'
    mocker.patch('requests.post', return_value=token_response)

    user_info_response = Response()
    user_info_response.status_code = 200
    user_info_response._content = b'{"id": "123456", "login": "johndoe"}'

    user_emails_response = Response()
    user_emails_response.status_code = 200
    user_emails_response._content = b'[{"email": "johndoe@example.com", "primary": true}]'

    mocker.patch('requests.get', side_effect=[user_info_response, user_emails_response])

    response = client.get(url, {'code': code})

    fetched_user = User.objects.get(email='johndoe@example.com')
    assert fetched_user.id == user.id

    fetched_token = Token.objects.get(user=user)
    assert fetched_token.key == token.key

    assert response.status_code == 200
    json_response = response.json()
    assert json_response['id'] == user.id
    assert json_response['username'] == user.username
    assert json_response['email'] == user.email
    assert json_response['registration_method'] == user.registration_method
    assert json_response['created'] is False
    assert json_response['token'] == token.key

