from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'place', 'time', 'action', 'is_pleasant', 'linked_habit', 'periodicity', 'reward',
                  'execution_time', 'is_public']
        read_only_fields = ['user']

    def validate_execution_time(self, value):
        if value > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")
        return value

    def validate_periodicity(self, value):
        if value < 7:
            raise serializers.ValidationError("Привычку нельзя выполнять реже, чем раз в 7 дней.")
        return value

    def validate(self, data):
        if data.get('reward') and data.get('linked_habit'):
            raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")
        if data.get('linked_habit') and not data['linked_habit'].is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")
        if data.get('is_pleasant') and (data.get('reward') or data.get('linked_habit')):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждения или связанную привычку.")
        return data
