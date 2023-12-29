from django.contrib import admin
from habits.models import Habit

@admin.register(Habit)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'place', 'schedule', 'is_public']
    list_filter = ['user', 'place', 'is_pleasant', 'is_public']
    fields = [
        'user',
        'place',
        'action',
        'schedule',
        'is_pleasant',
        'related_habit',
        'frequency',
        'reward',
        'duration',
        'is_public',
    ]
