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
        self.order = Order.objects.create(pizza=self.pizza,size='sm',customer=self.user, count= 1,status = 'de')
    

    def test_string_representation(self):
        '''
        test orders's string representation
        '''
        self.assertEqual(str("Margherita"), self.order.pizza.name)
        self.assertEqual(str("sm"), self.order.size)
        self.assertEqual(str("de"), self.order.status)
        self.assertEqual(str("test1"), self.order.customer.username)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Order._meta.verbose_name_plural),
                         "orders")
