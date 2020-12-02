from django.test import TestCase
from orders.models import Pizza, Order
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from orders.apiviews import OrderViewSet, PizzaViewSet


class TestPizzaTestCase(APITestCase):
    
    def setUp(self):
        
        self.factory = APIRequestFactory()
        self.view = PizzaViewSet.as_view({'get': 'list',
                                                  'post': 'create'})
        self.view_detail = PizzaViewSet.as_view({'get': 'retrieve',
                                                          'delete': 'destroy'})
        self.uri = '/pizzas/'
        self.test_user = self.setup_user()
        self.pizza = self.setup_pizza()


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
        pizza = Pizza.objects.create(name='Margherita')
        pizza.save()
        return pizza


    def test_create_pizza(self):
        '''
        test create pizza
        '''
        params = {
            'name': 'Marinara',
        }
        request = self.factory.post(self.uri, params)
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
        self.assertIn('Marinara', str(response.data))


    def test_create_already_existing_pizza(self):
        '''
        test create pizza already exist
        '''
        params = {
            'name': 'Margherita',
        }
        request = self.factory.post(self.uri, params)
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'
                         .format(response.status_code))
        self.assertIn('pizza with this name already exists',
                      str(response.data))


    def test_pizza_list(self):
        '''
        test retrieve all pizza
        '''
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.test_user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertIn('Margherita', str(response.data))


    def test_pizza_detail(self):
        '''
        test retrieve pizza detail
        '''
        pk = Pizza.objects.get(name="Margherita").pk
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.test_user)
        response = self.view_detail(request, pk=pk)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
        self.assertIn('Margherita', str(response.data))


    def test_pizza_not_existing_detail(self):
        '''
        test retrieve pizza detail when not existing
        '''
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.test_user)
        response = self.view_detail(request, pk=5000)
        self.assertEqual(response.status_code, 404,
                         'Expected Response Code 404, received {0} instead.'
                         .format(response.status_code))
        self.assertIn('Not found', str(response.data))


    def test_pizza_detail_destroy(self):
        '''
        test delete pizza detail
        '''
        pizza = Pizza.objects.get(name='Margherita')
        request = self.factory.delete(self.uri)
        force_authenticate(request, user=self.test_user)
        response = self.view_detail(request, pk=pizza.pk)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'
                         .format(response.status_code))
        self.assertNotIn('Margherita', str(response.data))
