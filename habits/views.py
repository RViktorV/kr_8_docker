from rest_framework import generics
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated

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
