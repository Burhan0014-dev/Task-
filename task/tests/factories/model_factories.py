import factory

from django.contrib.auth.hashers import make_password
from task.models import SGC, Services, User


class SGCFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SGC
    

    sgc_name = factory.Faker('uuid4')
    sgc_type = factory.Iterator(['A', 'B', 'C'])

class ServicesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Services

    service_name = factory.Faker('uuid4')
    service_details = factory.Faker('text', max_nb_chars=255)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('defaultpassword'))
    registration_method = factory.Iterator(['email', 'google', 'facebook', 'github'])
