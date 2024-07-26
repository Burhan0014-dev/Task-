from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser, Group, Permission

class SGC(models.Model):
    SGC_TYPE_CHOICES = (
        ('A', 'Type A'),
        ('B', 'Type B'),
        ('C', 'Type C'),
    )

    sgc_name = models.UUIDField(default=uuid4, editable=False)
    sgc_type = models.CharField(max_length=1, choices=SGC_TYPE_CHOICES)

    def __str__(self):
        return str(self.sgc_name)
    
class Services(models.Model):
    service_name= models.UUIDField(default=uuid4, editable=False)
    service_details = models.CharField(default= "It solutions", null=True, max_length=255, blank=True)

    def __str__(self):
        return str(self.service_name)



class User(AbstractUser):

    email = models.CharField(max_length=250, unique=True, null=False, blank=False)
    REGISTRATION_CHOICES = [
        ('email', 'Email'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
        ('github', 'Github'),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',  
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.pk is None and not self.password.startswith('pbkdf2_sha256$'):
            
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)