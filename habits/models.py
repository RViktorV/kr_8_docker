from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import Users


class Habit(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'is_pleasant': True})
    periodicity = models.PositiveIntegerField(default=1)  # in days
    reward = models.CharField(max_length=255, null=True, blank=True)
    execution_time = models.PositiveIntegerField(help_text="Time in seconds")
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.execution_time > 120:
            raise ValidationError(_('Время выполнения не может превышать 120 секунд.'))
        if self.reward and self.linked_habit:
            raise ValidationError(_('Можно установить только одно вознаграждение или связанную привычку.'))
        if self.periodicity < 7:
            raise ValidationError(_('Привычку нельзя выполнять реже, чем раз в 7 дней.'))
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(_('Приятная привычка не может иметь награды или связанной привычки.'))

    def __str__(self):
        return f'Habit: {self.action} at {self.time} in {self.place}'
