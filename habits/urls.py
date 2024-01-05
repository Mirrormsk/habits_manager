from habits.views import HabitViewSet
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = []

urlpatterns += router.urls

