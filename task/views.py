from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import SGC, Services, User
from .serializers import SGCSerializer, ServiceSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination, CursorPagination
from django.core.cache import cache
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from task.pagination_class import LargeResultsSetPagination



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    


class UserLoginView(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        
        if user:
            serializer = UserSerializer(user)
            return Response({'user': serializer.data})  
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class SGCRetrieveAPIView(RetrieveAPIView):
    
    pagination_class = CursorPagination
    
    queryset = SGC.objects.all()
    serializer_class = SGCSerializer
    

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SGCListAPIView(ListAPIView):
    queryset = SGC.objects.all()
    serializer_class = SGCSerializer

    def get_serializer_context(self): 
        context = super().get_serializer_context()
        services = Services.objects.all()
        context['services'] = services
        return context

class ServiceListAPIView(ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = LargeResultsSetPagination


class SGCCreateAPIView(CreateAPIView):
    queryset = SGC.objects.all()
    serializer_class = SGCSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class ServiceRetrieveAPIView(RetrieveAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer


class ServiceCreateAPIView(CreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
