from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")
        if data.get('execution_time') and data['execution_time'] > 120:
            raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд.")
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной.")
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждения или связанную привычку.")
        return data