# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase, APIClient
# from users.models import Users
# from habits.models import Habit
#
#
# class HabitTests(APITestCase):
#
#     def setUp(self):
#         # Создаем тестового пользователя
#         self.user = Users.objects.create_user(
#             email="testuser@example.com", password="password123", telegram_id="123456"
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)  # Авторизация для пользователя
#
#         # Создаем тестовую привычку
#         self.habit = Habit.objects.create(
#             user=self.user,
#             place="Park",
#             time="12:00",
#             action="Running",
#             is_pleasant=False,
#             periodicity=7,
#             execution_time=60,
#             is_public=True
#         )
#
#     def test_register_user(self):
#         """
#         Тестируем регистрацию нового пользователя.
#         """
#         url = reverse('register')
#         data = {
#             "email": "newuser@example.com",
#             "password": "newpassword123",
#             "telegram_id": "654321"
#         }
#         response = self.client.post(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Users.objects.filter(email="newuser@example.com").exists())
#
#     def test_create_habit(self):
#         """
#         Тестируем создание новой привычки.
#         """
#         url = reverse('habit-list')
#         data = {
#             "place": "Gym",
#             "time": "08:00",
#             "action": "Workout",
#             "is_pleasant": False,
#             "periodicity": 7,
#             "execution_time": 90,
#             "is_public": False,
#         }
#         response = self.client.post(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Habit.objects.filter(user=self.user).count(), 2)
#
#     def test_list_habits(self):
#         """
#         Тестируем получение списка привычек пользователя.
#         """
#         url = reverse('habit-list')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['action'], 'Running')
#
#     def test_list_public_habits(self):
#         """
#         Тестируем получение списка публичных привычек.
#         """
#         url = reverse('habit-public')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Проверяем, что публичная привычка возвращается
#
#     def test_update_habit(self):
#         """
#         Тестируем обновление привычки.
#         """
#         url = reverse('habit-detail', kwargs={'pk': self.habit.id})
#         data = {
#             'place': 'Updated Place',
#             'execution_time': 80
#         }
#         response = self.client.patch(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.habit.refresh_from_db()
#         self.assertEqual(self.habit.place, 'Updated Place')
#         self.assertEqual(self.habit.execution_time, 80)
#
#     def test_delete_habit(self):
#         """
#         Тестируем удаление привычки.
#         """
#         url = reverse('habit-detail', kwargs={'pk': self.habit.id})
#         response = self.client.delete(url)
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())
#
#     def test_invalid_execution_time(self):
#         """
#         Тестируем ошибку при указании времени выполнения больше 120 секунд.
#         """
#         url = reverse('habit-list')
#         data = {
#             "place": "Home",
#             "time": "14:00",
#             "action": "Meditation",
#             "is_pleasant": False,
#             "periodicity": 7,
#             "execution_time": 130,  # Некорректное время
#             "is_public": False,
#         }
#         response = self.client.post(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('execution_time', response.data)
#
#     def test_periodicity_validation(self):
#         """
#         Тестируем ошибку при указании периодичности меньше 7 дней.
#         """
#         url = reverse('habit-list')
#         data = {
#             "place": "Office",
#             "time": "09:00",
#             "action": "Reading",
#             "is_pleasant": False,
#             "periodicity": 3,  # Некорректная периодичность
#             "execution_time": 50,
#             "is_public": False,
#         }
#         response = self.client.post(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('periodicity', response.data)
#
#
# class HabitPublicTests(APITestCase):
#
#     def setUp(self):
#         # Создаем пользователей
#         self.user1 = Users.objects.create_user(email="user1@example.com", password="password123", telegram_id="111")
#         self.user2 = Users.objects.create_user(email="user2@example.com", password="password123", telegram_id="222")
#
#         # Создаем публичные и приватные привычки
#         Habit.objects.create(
#             user=self.user1, place="Park", time="12:00", action="Running",
#             is_pleasant=False, periodicity=7, execution_time=60, is_public=True
#         )
#         Habit.objects.create(
#             user=self.user2, place="Gym", time="08:00", action="Workout",
#             is_pleasant=False, periodicity=7, execution_time=90, is_public=False
#         )
#
#     def test_list_public_habits(self):
#         """
#         Тестируем получение только публичных привычек.
#         """
#         url = reverse('habit-public')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['action'], 'Running')
#
