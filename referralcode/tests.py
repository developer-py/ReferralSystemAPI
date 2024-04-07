from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import CustomUser

class UserRegistrationAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(reverse('user-registration'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().name, 'Test User')

class UserDetailAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(name='Test User', email='test@example.com', password='testpassword')

    def test_user_detail(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')

class AllUsersAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(name='Test User 1', email='test@example.com', password='testpassword')
        self.user2 = CustomUser.objects.create(name='Test User 2', email='test2@example.com', password='testpassword')

    def test_all_users(self):
        response = self.client.get(reverse('all-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(name='Test User', email='test@example.com', password='testpassword')

    def test_user_login_success(self):
        data = {'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(reverse('users-login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_user_login_invalid_credentials(self):
        data = {'email': 'invalid@example.com', 'password': 'invalidpassword'}
        response = self.client.post(reverse('users-login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReferralsAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create(name='Test User 1', email='test1@example.com', password='testpassword1')
        self.user2 = CustomUser.objects.create(name='Test User 2', email='test2@example.com', password='testpassword2', referred_by=self.user1)

    def test_referrals_api_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('referrals-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_referrals_api_unauthenticated(self):
        response = self.client.get(reverse('referrals-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
