from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import  MinValueValidator 
from enum import Enum
from datetime import datetime


class Pizza(models.Model):
    """
    docstring
    """
    name = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Order(models.Model):
    class STATUS(Enum):
        pending = ('pe', 'pending')
        delivered = ('de', 'delivered')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    class SIZES(Enum):
        small = ('sm', 'small')
        medium = ('md', 'medium')
        large = ('lg', 'large')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.CharField(max_length=2,choices=[x.value for x in SIZES], default='md')
    count = models.PositiveIntegerField(default=1,blank=False, validators=[MinValueValidator(1)])
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2,choices=[x.value for x in STATUS], default='pe')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.pizza.name

