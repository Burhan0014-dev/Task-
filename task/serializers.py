from rest_framework import serializers
from .models import SGC, Services, Users



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = '__all__'



class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = '__all__'  



class SGCSerializer(serializers.ModelSerializer):
    service_data = serializers.SerializerMethodField()

    class Meta:
        model = SGC
        fields = '__all__'

    def get_service_data(self, obj):
        
        
        try:
            services = self.context['services']
        except KeyError:
            
            return None
        data = next(
            (i for i in services if i.service_name == obj.sgc_name), {}
        )
        if data:
            service_serializer = ServiceSerializer(data)
            return service_serializer.data
        else:
            return None
        
    





