
# from task.views import SGCRetrieveAPIView, ServiceListAPIView, ServiceCreateAPIView, SGCListAPIView, ServiceRetrieveAPIView
from django.urls import path, include
from task.views import SGCRetrieveAPIView, SGCListAPIView, ServiceListAPIView , ServiceRetrieveAPIView, ServiceCreateAPIView,  SGCSListAPIView, SGCCreateAPIView, UserListView, UserRegistrationView, UserLoginView
from task.google_login import google_login, google_callback
from task.facebook_login import facebook_login, facebook_callback
from task.github_login import github_login, github_callback
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='log-in'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('sgc/', SGCListAPIView.as_view(), name='sgc-listl'),
    path('sgc/<int:pk>/', SGCRetrieveAPIView.as_view(), name='sgc-detail'),
    path('sgc/cache/', SGCSListAPIView.as_view(), name='sgc-cache'),
    path('sgc/create/', SGCCreateAPIView.as_view(), name='sgc-create'),
    path('services/', ServiceListAPIView.as_view(), name='service-listl'),
    path('service/<int:pk>/', ServiceRetrieveAPIView.as_view(), name='service-detail'),
    path('service/create/', ServiceCreateAPIView.as_view(), name='service-create'),
    path('login/google/', google_login, name='google_login'),
    path('login/google/callback/', google_callback, name='google_callback'),
    path('users/', UserListView.as_view(), name='users'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('facebook/login/', facebook_login, name='facebook_login'),
    path('facebook/callback/', facebook_callback, name='facebook_callback'),
    path('github/login/', github_login, name='github_login'),
    path('github/callback/', github_callback, name='github_callback'),
]
