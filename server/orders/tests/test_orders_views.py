from django.test import TestCase
from rest_framework import response
from orders.models import Pizza, Order
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from orders.apiviews import OrderViewSet, PizzaViewSet
import json



class TestOrderTestCase(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.order_view = OrderViewSet.as_view({'get': 'list',
                                                         'post': 'create'})
        self.single_order_view = OrderViewSet.as_view(
            {'get': 'retrieve','patch': 'partial_update', 'delete': 'destroy'}
        )
        self.pizza_uri = '/pizzas/'
        self.order_uri = '/orders/'
        #self.public_recipes_uri = '/public-recipes/'
        self.test_user = self.setup_user()
        self.pizza = self.setup_pizza()
        self.order = self.setup_order()
        self.order_data =  {"size": "sm","count": 9,"status": "de","pizza": self.pizza.id,"customer": self.test_user.id}

    
    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            username='test1',
            email='test1@test.com',
            password='test12345'
        )
    
    @staticmethod
    def setup_pizza():
        pizza = Pizza.objects.create(
            name='Margherita',
        )
        pizza.save()
        return pizza
    
    @staticmethod
    def setup_order():
        order = Order.objects.create(
            pizza=Pizza.objects.get(name='Margherita'),
            size='sm',
            customer=get_user_model().objects.get(username='test1'), 
            count= 1,
            status = 'de'
        )
        order.save()
        return order

    def test_get_only_one_order_at_start(self):
        """
        test starts with only one order
        """
        request = self.factory.get(self.order_uri)
        force_authenticate(request, user=self.test_user)
        response = self.order_view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(len(response.data), 1)
    
    
    def test_order_list(self):
        '''
        test retrieve all order
        '''
        request = self.factory.get(self.order_uri)
        force_authenticate(request, user=self.test_user)
        response = self.order_view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertIn('Margherita', str(response.data))

    def test_create_single_order(self):
        """
        test create single order
        """
        request = self.factory.post(self.order_uri, self.order_data)
        force_authenticate(request, user=self.test_user)
        response = self.order_view(request)
        self.assertEqual(response.status_code, 201,
                    'Expected Response Code 201, received {0} instead.'
                    .format(response.status_code))

    def test_create_bulk_order(self):
        """
        test bulk upload of order
        """
        request = self.factory.post(self.order_uri, json.dumps([
            {"size": "sm","count": 1,"status": "pe","pizza": self.pizza.id,"customer": self.test_user.id},
            {"size": "sm","count": 1,"status": "de","pizza": self.pizza.id,"customer": self.test_user.id}]),
            content_type='application/json')
        force_authenticate(request, user=self.test_user)
        response = self.order_view(request)
        self.assertEqual(response.status_code, 201,
                    'Expected Response Code 201, received {0} instead.'
                    .format(response.status_code))

    def test_filter_order_by_status(self):
        """
        test filter order by status
        """
        Order.objects.create(
            pizza=self.pizza,
            size='sm',
            customer=self.test_user, 
            count= 1,
            status = 'pe'
        )
        Order.objects.create(
            pizza=self.pizza,
            size='sm',
            customer=self.test_user, 
            count= 1,
            status = 'pe'
        )
        request = self.factory.get(self.order_uri, {"status":"pe"})
        force_authenticate(request, user=self.test_user)
        response = self.order_view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(len(response.data), 2)

    def test_filter_order_by_customer(self):
        """
        test filter order by customer
        """
        Order.objects.create(
            pizza=self.pizza,
            size='sm',
            customer=self.test_user, 
            count= 1,
            status = 'pe'
        )
        Order.objects.create(
            pizza=self.pizza,
            size='sm',
            customer=self.test_user, 
            count= 1,
            status = 'pe'
        )
        request = self.factory.get(self.order_uri, {"customer_id":self.test_user.id})
        force_authenticate(request, user=self.test_user)
        response = self.order_view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertEqual(len(response.data), 3)



    def test_update_single_order(self):
        """
        test update single order
        """
        request = self.factory.patch('/orders/', self.order_data, )
        force_authenticate(request, user=self.test_user)
        response =  self.single_order_view(request, pk=self.order.id)
        self.assertEqual(response.status_code, 200,
                    'Expected Response Code 201, received {0} instead.'
                    .format(response.status_code))

    def test_can_not_update_after_delivery(self):
        """
        test can not update after delivery
        """
        request = self.factory.patch('/orders/', {"size": "sm","count": 9,"status": "pe","pizza": 1,"customer": self.test_user.id}, )
        force_authenticate(request, user=self.test_user)
        response =  self.single_order_view(request, pk=self.order.id)
        self.assertEqual(response.status_code, 403,
                    'Expected Response Code 403, received {0} instead.'
                    .format(response.status_code))
    
    def test_retrive_single_order(self):
        '''
        test retrieve a single order
        '''
        request = self.factory.get(self.order_uri)
        force_authenticate(request, user=self.test_user)
        pk = Order.objects.filter(pizza__name='Margherita', customer=self.test_user)[0].pk
        response = self.single_order_view(request, pk=pk)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))


    def test_delete_single_order(self):
        '''
        test retrieve a single order
        '''
        request = self.factory.delete(self.order_uri)
        force_authenticate(request, user=self.test_user)
        pk = Order.objects.filter(pizza__name='Margherita', customer=self.test_user)[0].pk
        response = self.single_order_view(request, pk=pk)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))


    
    def test_get_single_order_not_found(self):
        '''
        test retrieve a single order not found
        '''
        request = self.factory.get(self.order_uri)
        force_authenticate(request, user=self.test_user)
        response = self.single_order_view(request, pk=3000)
        self.assertEqual(response.status_code, 404,
                         'Expected Response Code 404, received {0} instead.'
                         .format(response.status_code))
        self.assertNotIn('Margherita', str(response.data))

    def test_delete_single_order(self):
        '''
        test delete single order
        '''
        request = self.factory.delete(self.order_uri)
        force_authenticate(request, user=self.test_user)
        pk = Order.objects.filter(pizza__name='Margherita', customer=self.test_user)[0].pk
        response = self.single_order_view(request, pk=pk)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))




    
   