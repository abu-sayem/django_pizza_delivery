from rest_framework import serializers

from .models import Order, Pizza
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',]

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        #fields = '__all__'
        exclude = ('created_at','updated_at' )


class OrderSerializerCreateRetrive(serializers.ModelSerializer):
    flavor = serializers.CharField(source='pizza.name')
    customer = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['flavor','size','count','customer', 'status']

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        #fields = '__all__'
        exclude = ('created_at','updated_at' )
