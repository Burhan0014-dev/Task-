import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from task.models import User, SGC, Services
from task.tests.factories.model_factories import UserFactory, ServicesFactory, SGCFactory
from task.serializers import SGCSerializer, UserSerializer, ServiceSerializer
from django.contrib.auth import authenticate
from task.views import UserLoginView, SGCListAPIView


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_sgc():
    return SGCFactory.create()

@pytest.fixture
def create_services():
    return ServicesFactory.create_batch(3)

@pytest.fixture
def create_service():
    return ServicesFactory.create()

@pytest.fixture
def create_users():
    return UserFactory.create_batch(5)
@pytest.fixture
def sgc_data():
    return {
        'sgc_type': 'A',
    }


@pytest.mark.django_db
def test_add_sgc(api_client, sgc_data):
    url = reverse('sgc-create')  
    response = api_client.post(url, sgc_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert SGC.objects.filter(sgc_type=response.data.get("sgc_type"))


@pytest.mark.django_db
def test_sgc_list_view(api_client, create_sgc):
    # Create some SGC instances
    sgcs = [SGCFactory.create() for _ in range(5)]

    services = [ServicesFactory.create(service_name=sgc.sgc_name) for sgc in sgcs]

    url = reverse('sgc-list')
    response = api_client.get(url)

    expected_sgc = SGC.objects.all()
    services = Services.objects.all()
    serializer_sgc = SGCSerializer(expected_sgc, many=True, context={'services': services}).data
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response_data, list)  


@pytest.mark.django_db
def test_sgc_retrieve_api_view(api_client, create_sgc):
    """Tests successful retrieval of a SGC."""
    sgc = create_sgc

    url = reverse('sgc-detail', kwargs={'pk': sgc.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    view_queryset = SGC.objects.all()
    retrieved_sgc = view_queryset.get(pk=sgc.pk)
    services = Services.objects.all()
    expected_data = SGCSerializer(retrieved_sgc, context={'services': services}).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_add_service(api_client):
    url = reverse('service-create')  
    data = {
        'service_details': 'Test Details',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Services.objects.filter(service_name=response.data.get("service_name"))

@pytest.mark.django_db
def test_service_list_pagination():
    services = [ServicesFactory.create() for _ in range(5)]

    client = APIClient()
    url = reverse('service-list')

    # Test pagination - first page
    response = client.get(url, {'page': 1, 'page_size': 2})
    assert response.status_code == status.HTTP_200_OK
    assert 'page_count' in response.data
    assert 'next' in response.data
    assert 'previous' in response.data
    assert 'results' in response.data
    assert response.data['page_count'] == 3  # 5 items, 2 per page
    assert response.data['results'] == ServiceSerializer(Services.objects.all()[:2], many=True).data

    # Test pagination - second page
    response = client.get(url, {'page': 2, 'page_size': 2})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == ServiceSerializer(Services.objects.all()[2:4], many=True).data

    # Test pagination - third page
    response = client.get(url, {'page': 3, 'page_size': 2})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'] == ServiceSerializer(Services.objects.all()[4:], many=True).data

    # Test pagination - page_size larger than max_page_size
    response = client.get(url, {'page_size': 200})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 5

@pytest.mark.django_db
def test_service_retrieve_api_view(api_client, create_service):
    """Tests successful retrieval of a service."""
    service = create_service

    url = reverse('service-detail', kwargs={'pk': service.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    view_queryset = Services.objects.all()
    retrieved_service = view_queryset.get(pk=service.pk)
    expected_data = ServiceSerializer(retrieved_service).data
    assert response.data == expected_data


@pytest.mark.django_db
def test_user_list_view(api_client, create_users):
    url = reverse('users')
    response = api_client.get(url)

    
    expected_users = User.objects.all()
    serialized_users = UserSerializer(expected_users, many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialized_users


@pytest.mark.django_db
def test_user_login_view_valid_credentials(api_client):
    """Tests successful login with valid credentials."""
    data = {
        "username": 'test_user',
        "password": "Pasword1",
        "email": "random@gmail.com"
    }
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        assert False

    response = api_client.post('/login/', data=data, format='json')  
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_user_login_view_invalid_credentials(api_client):
    """Tests unsuccessful login with invalid credentials."""

    username = 'invalid_user'
    password = 'wrong_password'
    data = {'username': username, 'password': password}
    response = api_client.post('/login/', data=data, format='json')  

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'error' in response.data
    assert response.data['error'] == 'Invalid credentials'  

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('register')  
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser").exists()


