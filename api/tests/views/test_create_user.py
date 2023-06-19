from django.test import TestCase
from django.urls import reverse

class CreateUserTest(TestCase):
    def create_user_success(self):
        """
            Test create new user with valid data
        """
        data = {
            'full_name': 'test',
            'email': 'test@gmail.com',
            'password': 'test123'
        }
        response = self.client.post(reverse('create_user'), data=data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'User created')