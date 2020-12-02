from django.test import TestCase
from orders.models import Pizza, Order
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from orders.apiviews import OrderViewSet, PizzaViewSet


class TestPizzaModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="test",
            last_name="user",
            username='test1',
            email='test1@test.com',
            password='test12345'
        )

        self.pizza = Pizza.objects.create(
            name='Margherita',
        )
    
    def test_pizza_name(self):
        self.assertEqual(self.pizza.name, 'Margherita')

    def test_string_representation(self):
        '''
        test pizza's string representation
        '''
        pizza = Pizza(
            name="Margherita"
        )
        self.assertEqual(str("Margherita"), pizza.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Pizza._meta.verbose_name_plural),
                         "pizzas")
