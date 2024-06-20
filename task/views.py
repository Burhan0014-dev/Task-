from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import SGC, Services, Users
from .serializers import SGCSerializer, ServiceSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        
        if user:
            serializer = UserSerializer(user)
            token, created = Token.objects.get_or_create(user=user)  
            return Response({'user': serializer.data, 'token': token.key})  
        else:
            return Response({'error': 'Invalid credentials'}, status=401)






class SGCRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    
    queryset = SGC.objects.all()
    serializer_class = SGCSerializer
    

class UserListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class SGCListAPIView(ListAPIView):
    queryset = SGC.objects.all()
    serializer_class = SGCSerializer

    def get_serializer_context(self): 
        context = super().get_serializer_context()
        services = Services.objects.all()
        context['services'] = services
        return context

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1 
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        page_count = self.page.paginator.num_pages
        return Response({
            'page_count': page_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class ServiceListAPIView(ListAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = LargeResultsSetPagination


class SGCSListAPIView(ListAPIView):
    serializer_class = SGCSerializer 
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        #return SGC.objects.all()
        return SGC.objects.all().order_by('id')


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
 
        cached_services = cache.get('cached_services')
        if cached_services is None:  
            services = Services.objects.all()
            cache.set('cached_services', services)
        else:
            services = cached_services

        page = self.paginate_queryset(queryset)
        if page is not None:
            
            sgc_data = SGCSerializer(page, many=True, context={"services": list(services)}).data
            cached_service_data = ServiceSerializer(services, many=True).data

            return self.get_paginated_response({
                'sgc_data': sgc_data,
                'cached_service_data': cached_service_data
            })

        sgc_data = SGCSerializer(page, many=True, context={"services": list(services)}).data
        cached_service_data = ServiceSerializer(services, many=True).data
        return Response({
            'sgc_data': sgc_data,
            'cached_service_data': cached_service_data
        })



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

class ServiceListAPIView(ListAPIView):
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
