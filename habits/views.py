from requests import Response
from rest_framework import generics, viewsets
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .tasks import send_telegram_message


class HabitPagination(PageNumberPagination):
    page_size = 5

class HabitListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка привычек и создания новой привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ограничиваем список привычек пользователем, отправившим запрос
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Привязываем новую привычку к текущему пользователю
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления или удаления конкретной привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ограничиваем доступ к привычкам, принадлежащим текущему пользователю
        return Habit.objects.filter(user=self.request.user)


# Задача для отправки напоминаний в Telegram
class ReminderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def send_reminder(self, request, habit_id):
        habit = Habit.objects.get(id=habit_id, user=request.user)
        # Здесь можно передать нужный чат-ид пользователя в Telegram
        chat_id = request.user.profile.telegram_chat_id  # предполагается, что есть поле в профиле
        send_telegram_message.delay(habit_id, chat_id)
        return Response({'status': 'Напоминание отправлено!'})


class PublicHabitListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination
