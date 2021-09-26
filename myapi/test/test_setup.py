from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

class TestSetUp(APITestCase):

    def setup(self):
        self.register_url = reverse('auth/register')
        self.login_url = reverse('token_obtain_pair')

        user_data = {

        }
        return super().setup()

    def teardown(self):
        return super().teadown()
    