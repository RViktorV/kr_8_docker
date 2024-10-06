from rest_framework import viewsets
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user)
        return super().get_queryset()
