from django.db import models


class Habit(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    place = models.CharField(max_length=155, verbose_name="место")
    action = models.CharField(max_length=155, verbose_name="действие")
    schedule = models.TimeField(verbose_name="время")
    is_pleasant = models.BooleanField(verbose_name="приятная")
    related_habit = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name="связана", null=True, blank=True
    )
    frequency = models.PositiveSmallIntegerField(
        verbose_name="периодичность (дни)", default=1
    )
    reward = models.CharField(max_length=255, verbose_name="награда", null=True, blank=True)
    duration = models.DurationField(verbose_name="продолжительность")
    is_public = models.BooleanField(verbose_name="публичная", default=False)
    last_sent = models.DateTimeField(verbose_name="отправлено", null=True, blank=True)

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f"{self.action}"
