from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import Users


class UsersTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Создаем тестового пользователя для проверки авторизации
        self.user = Users.objects.create_user(
            email="testuser@example.com", password="password123", telegram_id="123456"
        )
        self.user.set_password("password")  # Убедитесь, что пароль хеширован
        self.user.save()

    def test_get_users_list(self):
        """
        Тестируем получение списка пользователей.
        """
        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        """
        Тестируем регистрацию нового пользователя.
        """
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "telegram_id": "654321"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Users.objects.filter(email="newuser@example.com").exists())

    def test_login_user(self):
        """
        Тестируем получение JWT токена при входе.
        """
        url = reverse('login')
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """
        Тестируем обновление JWT токена.
        """
        # Получаем первоначальный токен
        login_url = reverse('login')
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']

        # Проверяем обновление токена
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_user_list(self):
        """
        Тестируем получение списка пользователей.
        """
        # Авторизуемся с помощью токена
        self.client.force_authenticate(user=self.user)
        url = reverse('users-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_user_detail(self):
        """
        Тестируем получение деталей конкретного пользователя.
        """
        # Авторизуемся с помощью токена
        self.client.force_authenticate(user=self.user)
        url = reverse('users-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_user(self):
        """
        Тестируем обновление данных пользователя.
        """
        # Авторизуемся с помощью токена
        self.client.force_authenticate(user=self.user)
        url = reverse('users-detail', kwargs={'pk': self.user.id})
        data = {
            'city': 'New City'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'New City')

    def test_delete_user(self):
        """
        Тестируем удаление пользователя.
        """
        # Авторизуемся с помощью токена
        self.client.force_authenticate(user=self.user)
        url = reverse('users-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Users.objects.filter(id=self.user.id).exists())
